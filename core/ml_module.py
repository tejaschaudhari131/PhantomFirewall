import logging
from typing import Dict, List
import numpy as np
from sklearn.ensemble import IsolationForest
from collections import deque

class MLModule:
    def __init__(self, window_size: int = 1000):
        self.logger = logging.getLogger(__name__)
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.window_size = window_size
        self.packet_history = deque(maxlen=window_size)
        self.is_trained = False
        
    def _extract_features(self, packet_info: Dict) -> np.ndarray:
        """Extract relevant features from packet info for ML model."""
        features = []
        
        # Convert IP to numerical representation
        ip_parts = list(map(int, packet_info['source_ip'].split('.')))
        features.extend(ip_parts)
        
        # Add protocol as feature
        features.append(packet_info['protocol'])
        
        # Add time-based features
        hour = packet_info['timestamp'].hour
        minute = packet_info['timestamp'].minute
        features.extend([hour, minute])
        
        return np.array(features).reshape(1, -1)
    
    def train(self, packet_history: List[Dict]):
        """Train the ML model on historical packet data."""
        try:
            if len(packet_history) < self.window_size // 2:
                self.logger.warning("Not enough data for training")
                return
            
            features = np.vstack([self._extract_features(packet) for packet in packet_history])
            self.model.fit(features)
            self.is_trained = True
            self.logger.info("ML model training completed")
            
        except Exception as e:
            self.logger.error(f"Error training ML model: {str(e)}")
    
    def predict(self, packet_info: Dict) -> str:
        """Predict whether a packet should be accepted or dropped."""
        try:
            # Add to history
            self.packet_history.append(packet_info)
            
            # Train model if we have enough data and haven't trained yet
            if not self.is_trained and len(self.packet_history) >= self.window_size:
                self.train(list(self.packet_history))
            
            # If not trained yet, accept all packets
            if not self.is_trained:
                return 'ACCEPT'
            
            # Extract features and predict
            features = self._extract_features(packet_info)
            prediction = self.model.predict(features)[0]
            
            # IsolationForest returns 1 for normal data and -1 for anomalies
            return 'ACCEPT' if prediction == 1 else 'DROP'
            
        except Exception as e:
            self.logger.error(f"Error in ML prediction: {str(e)}")
            return 'ACCEPT'  # Accept on error
    
    def update(self, packet_info: Dict, label: str):
        """Update the model with new labeled data."""
        try:
            self.packet_history.append(packet_info)
            
            # Retrain model periodically
            if len(self.packet_history) >= self.window_size:
                self.train(list(self.packet_history))
                
        except Exception as e:
            self.logger.error(f"Error updating ML model: {str(e)}")
