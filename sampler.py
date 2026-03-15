# This program simulates the operation of a weather station's sampler.
# A sampler is composed of multiple sensors, 
# for example it could be an entire weather tower or satellite

import time
from datetime import datetime
from sensor import Sensor
import requests  

NODE_URL = "http://localhost:3000/sample"  # Node sampler endpoint

class Sampler:
    '''
    Samples voltage readings from the Sensor and attaches timestamps.
    '''
    def __init__(self, num_sensors=10):
        self.sensor_list = [Sensor() for _ in range(num_sensors)]

    def sample(self):
        '''
        Take a sample from each sensor and return structured data.
        '''
        # Note: This is the ideal way to send the timestamp in a JSON serializable way
        timestamp = int(datetime.now().timestamp())
        # Each sensor in the sampling unit will take a voltage reading
        voltage_list = [sensor.read_voltage() for sensor in self.sensor_list]

        # Many valid solutions for passing this data along, dictionary is fine
        sample_data = {
            'timestamp': timestamp,
            'voltage': voltage_list
        }
        return sample_data

def send_to_node(data):
    '''
    Send sample data to Node.js sampler automatically
    '''
    try:
        requests.post(NODE_URL, json=data)
    except Exception as e:
        print(f"Failed to send data to Node: {e}")

if __name__ == '__main__':
    sampler = Sampler(num_sensors=10) 
    while True:
        sample_data = sampler.sample()
        print(sample_data)
        send_to_node(sample_data)  # Send automatically
        time.sleep(2)  # Match your sampling interval