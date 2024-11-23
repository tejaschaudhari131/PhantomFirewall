import unittest  
import requests  

class TestAPIEndpoints(unittest.TestCase):  

    BASE_URL = "http://localhost:8080/api/v1"  

    def test_status_endpoint(self):  
        response = requests.get(f"{self.BASE_URL}/status")  
        self.assertEqual(response.status_code, 200)  
        self.assertIn("status", response.json())  

    def test_add_rule(self):  
        payload = {  
            "name": "Block SSH",  
            "priority": 1,  
            "action": "DROP",  
            "protocol": "TCP",  
            "port": 22  
        }  
        response = requests.post(f"{self.BASE_URL}/rules", json=payload)  
        self.assertEqual(response.status_code, 201)  
        self.assertIn("id", response.json())  

    def test_remove_rule(self):  
        rule_id = 1  # Assuming rule 1 exists  
        response = requests.delete(f"{self.BASE_URL}/rules/{rule_id}")  
        self.assertEqual(response.status_code, 204)  

if __name__ == "__main__":  
    unittest.main()  
