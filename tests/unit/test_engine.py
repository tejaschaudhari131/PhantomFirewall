import unittest  
from core.engine import PacketProcessor  

class TestPacketProcessor(unittest.TestCase):  

    def setUp(self):  
        self.processor = PacketProcessor()  

    def test_process_valid_packet(self):  
        packet = {  
            "source_ip": "192.168.1.1",  
            "destination_ip": "192.168.1.2",  
            "protocol": "TCP",  
            "port": 80  
        }  
        result = self.processor.process_packet(packet)  
        self.assertEqual(result, "ACCEPT")  

    def test_process_blocked_packet(self):  
        packet = {  
            "source_ip": "10.0.0.1",  
            "destination_ip": "192.168.1.2",  
            "protocol": "TCP",  
            "port": 22  
        }  
        self.processor.add_rule({  
            "action": "DROP",  
            "source_ip": "10.0.0.1"  
        })  
        result = self.processor.process_packet(packet)  
        self.assertEqual(result, "DROP")  

if __name__ == "__main__":  
    unittest.main()  
