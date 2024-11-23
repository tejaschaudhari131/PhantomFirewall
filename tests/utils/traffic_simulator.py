import random  

def simulate_traffic(num_packets=100):  
    protocols = ["TCP", "UDP", "ICMP"]  
    ports = range(1, 65536)  

    traffic = []  
    for _ in range(num_packets):  
        packet = {  
            "source_ip": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",  
            "destination_ip": f"10.0.{random.randint(0, 255)}.{random.randint(0, 255)}",  
            "protocol": random.choice(protocols),  
            "port": random.choice(ports)  
        }  
        traffic.append(packet)  

    return traffic  

if __name__ == "__main__":  
    print(simulate_traffic(10))  
