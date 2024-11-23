import unittest  
from core.ml_module import AnomalyDetector  

class TestAnomalyDetector(unittest.TestCase):  

    def setUp(self):  
        self.detector = AnomalyDetector(window_size=1000, contamination=0.1)  

    def test_anomaly_detection(self):  
        traffic_data = [100, 200, 150, 5000, 120, 110]  # Simulated traffic  
        anomalies = self.detector.detect(traffic_data)  
        self.assertEqual(len(anomalies), 1)  

    def test_update_model(self):  
        new_data = [50, 60, 70, 80, 90]  
        self.detector.update_model(new_data)  
        self.assertIsNotNone(self.detector.model)  

if __name__ == "__main__":  
    unittest.main()  
