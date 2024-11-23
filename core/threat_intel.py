import logging
import requests
from typing import Set, Dict
from datetime import datetime, timedelta
import threading
import time

class ThreatIntelligence:
    def __init__(self, update_interval: int = 3600):
        self.logger = logging.getLogger(__name__)
        self.malicious_ips: Set[str] = set()
        self.last_update = datetime.min
        self.update_interval = update_interval
        self.update_lock = threading.Lock()
        
        # Start background updater
        self.updater_thread = threading.Thread(target=self._background_update)
        self.updater_thread.daemon = True
        self.updater_thread.start()
    
    def _fetch_threat_feeds(self) -> Set[str]:
        """Fetch and aggregate threat intelligence from multiple sources."""
        malicious_ips = set()
        
        # AlienVault OTX
        try:
            response = requests.get(
                "https://otx.alienvault.com/api/v1/pulses/subscribed",
                headers={"X-OTX-API-KEY": "YOUR_API_KEY"}
            )
            if response.status_code == 200:
                data = response.json()
                for pulse in data.get('results', []):
                    for indicator in pulse.get('indicators', []):
                        if indicator['type'] == 'IPv4':
                            malicious_ips.add(indicator['indicator'])
        except Exception as e:
            self.logger.error(f"Error fetching AlienVault feed: {str(e)}")
        
        # AbuseIPDB
        try:
            response = requests.get(
                "https://api.abuseipdb.com/api/v2/blacklist",
                headers={"Key": "YOUR_API_KEY"},
                params={"confidenceMinimum": 90}
            )
            if response.status_code == 200:
                data = response.json()
                for ip_data in data.get('data', []):
                    malicious_ips.add(ip_data['ipAddress'])
        except Exception as e:
            self.logger.error(f"Error fetching AbuseIPDB feed: {str(e)}")
        
        return malicious_ips
    
    def _update_threat_intel(self):
        """Update threat intelligence data."""
        try:
            with self.update_lock:
                new_ips = self._fetch_threat_feeds()
                self.malicious_ips = new_ips
                self.last_update = datetime.now()
                self.logger.info(f"Updated threat intelligence: {len(self.malicious_ips)} malicious IPs")
        except Exception as e:
            self.logger.error(f"Error updating threat intelligence: {str(e)}")
    
    def _background_update(self):
        """Background thread for periodic updates."""
        while True:
            if datetime.now() - self.last_update > timedelta(seconds=self.update_interval):
                self._update_threat_intel()
            time.sleep(60)  # Check every minute
    
    def is_malicious(self, ip: str) -> bool:
        """Check if an IP is known to be malicious."""
        with self.update_lock:
            return ip in self.malicious_ips
    
    def add_ip(self, ip: str):
        """Manually add an IP to the threat intelligence."""
        with self.update_lock:
            self.malicious_ips.add(ip)
            self.logger.info(f"Added IP to threat intelligence: {ip}")
    
    def remove_ip(self, ip: str):
        """Manually remove an IP from the threat intelligence."""
        with self.update_lock:
            self.malicious_ips.discard(ip)
            self.logger.info(f"Removed IP from threat intelligence: {ip}")
