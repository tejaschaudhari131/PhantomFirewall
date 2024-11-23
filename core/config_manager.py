import yaml
import logging
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FirewallConfig:
    mode: str
    learning_rate: float
    update_interval: int
    log_level: str
    api_port: int
    dashboard_port: int

class ConfigManager:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path
        self.config: Optional[FirewallConfig] = None
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
                
            self.config = FirewallConfig(
                mode=config_data.get('mode', 'adaptive'),
                learning_rate=float(config_data.get('learning_rate', 0.01)),
                update_interval=int(config_data.get('update_interval', 3600)),
                log_level=config_data.get('log_level', 'INFO'),
                api_port=int(config_data.get('api_port', 8080)),
                dashboard_port=int(config_data.get('dashboard_port', 3000))
            )
            
            self._setup_logging()
            self.logger.info("Configuration loaded successfully")
            
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            raise

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "phantom.log"),
                logging.StreamHandler()
            ]
        )

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            config_dict = {
                'mode': self.config.mode,
                'learning_rate': self.config.learning_rate,
                'update_interval': self.config.update_interval,
                'log_level': self.config.log_level,
                'api_port': self.config.api_port,
                'dashboard_port': self.config.dashboard_port
            }
            
            with open(self.config_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False)
                
            self.logger.info("Configuration saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
            raise

    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values."""
        try:
            for key, value in updates.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                else:
                    self.logger.warning(f"Unknown configuration key: {key}")
            
            self.save_config()
            self.logger.info("Configuration updated successfully")
            
        except Exception as e:
            self.logger.error(f"Error updating configuration: {str(e)}")
            raise

    def get_config(self) -> FirewallConfig:
        """Get current configuration."""
        return self.config
