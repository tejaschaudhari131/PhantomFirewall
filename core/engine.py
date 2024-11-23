import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import netfilterqueue
import scapy.all as scapy
from .ml_module import MLModule
from .threat_intel import ThreatIntelligence

@dataclass
class Rule:
    name: str
    priority: int
    action: str  # "ACCEPT", "DROP", "LOG"
    protocol: Optional[str] = None
    port: Optional[int] = None
    source_ip: Optional[str] = None
    dest_ip: Optional[str] = None

class FirewallEngine:
    def __init__(self, config_path: str):
        self.logger = logging.getLogger(__name__)
        self.rules: List[Rule] = []
        self.ml_module = MLModule()
        self.threat_intel = ThreatIntelligence()
        self.packet_queue = netfilterqueue.NetfilterQueue()
        self.load_config(config_path)
        
    def load_config(self, config_path: str) -> None:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                import yaml
                config = yaml.safe_load(f)
                
            # Parse rules from config
            for rule_config in config.get('rules', []):
                rule = Rule(**rule_config)
                self.rules.append(rule)
                
            self.rules.sort(key=lambda x: x.priority)
            self.logger.info(f"Loaded {len(self.rules)} rules")
        except Exception as e:
            self.logger.error(f"Failed to load config: {str(e)}")
            raise

    def process_packet(self, packet):
        """Process a single packet and decide its fate."""
        try:
            # Convert netfilterqueue packet to scapy packet for easier handling
            scapy_packet = scapy.IP(packet.get_payload())
            
            # Extract packet information
            packet_info = {
                'source_ip': scapy_packet.src,
                'dest_ip': scapy_packet.dst,
                'protocol': scapy_packet.proto,
                'timestamp': datetime.now()
            }
            
            # Check threat intelligence
            if self.threat_intel.is_malicious(packet_info['source_ip']):
                self.logger.warning(f"Blocked malicious IP: {packet_info['source_ip']}")
                packet.drop()
                return
            
            # Get ML model prediction
            ml_decision = self.ml_module.predict(packet_info)
            if ml_decision == 'DROP':
                self.logger.info(f"ML model suggested blocking packet from {packet_info['source_ip']}")
                packet.drop()
                return
            
            # Apply rules
            for rule in self.rules:
                if self._packet_matches_rule(packet_info, rule):
                    if rule.action == 'ACCEPT':
                        packet.accept()
                    elif rule.action == 'DROP':
                        packet.drop()
                    elif rule.action == 'LOG':
                        self.logger.info(f"Logged packet: {packet_info}")
                        packet.accept()
                    return
            
            # Default action: accept
            packet.accept()
            
        except Exception as e:
            self.logger.error(f"Error processing packet: {str(e)}")
            packet.accept()  # Accept on error to prevent network disruption
    
    def _packet_matches_rule(self, packet_info: Dict, rule: Rule) -> bool:
        """Check if a packet matches a rule."""
        if rule.protocol and packet_info['protocol'] != rule.protocol:
            return False
        if rule.source_ip and packet_info['source_ip'] != rule.source_ip:
            return False
        if rule.dest_ip and packet_info['dest_ip'] != rule.dest_ip:
            return False
        # Add more matching criteria as needed
        return True
    
    def start(self):
        """Start the firewall engine."""
        try:
            self.packet_queue.bind(1, self.process_packet)
            self.logger.info("Firewall engine started")
            self.packet_queue.run()
        except KeyboardInterrupt:
            self.logger.info("Firewall engine stopped by user")
        except Exception as e:
            self.logger.error(f"Firewall engine error: {str(e)}")
        finally:
            self.packet_queue.unbind()
    
    def stop(self):
        """Stop the firewall engine."""
        try:
            self.packet_queue.unbind()
            self.logger.info("Firewall engine stopped")
        except Exception as e:
            self.logger.error(f"Error stopping firewall: {str(e)}")
