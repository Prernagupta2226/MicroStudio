import requests
import time

# Service Details
service_name = 'microservice1'
service_address = 'http://localhost:5002'

# Register service
def register_service():
    payload = {
        'service_name': service_name,
        'service_address': service_address
    }
    response = requests.post("http://localhost:5001/register", json=payload)
    print(response.json())

# Send Heartbeat
def send_heartbeat():
    payload = {
        'service_name': service_name
    }
    response = requests.post("http://localhost:5001/heartbeat", json=payload)
    print(response.json())

# Discover services
def discover_services():
    response = requests.get("http://localhost:5001/services")
    print("Available services:", response.json())

# Main logic for testing
if __name__ == "__main__":
    # Register the service
    register_service()

    # Simulate sending heartbeats and discovering services
    while True:
        time.sleep(2 * 60)  # 2 minutes
        send_heartbeat()

        discover_services()