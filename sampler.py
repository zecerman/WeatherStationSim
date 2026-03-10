# This program simulates the operation of a weather station's sampler.
# A sampler is composed of multiple sensors, 
# for example it could be an entire weather tower or satellite

import time
from datetime import datetime
from sensor import Sensor


class Sampler:
    '''
    Samples voltage readings from the Sensor and attaches timestamps.
    '''

    def __init__(self):
        self.sensor_list = []
        # TODO 10 sensors per sampler is currently hard coded, 
        # could easily be changed to a dynamic number
        for _ in range(10):
            self.sensor_list.append(Sensor())

    def sample(self):
        '''
        Take a sample from each sensor and return structured data.
        '''
        # Note: This is the ideal way to send the timestamp in a JSON serializable way
        timestamp = datetime.now().timestamp()
        # Each sensor in the sampling unit will take a voltage reading
        voltage_list = []
        for sensor in self.sensor_list:
            voltage_list.append(sensor.read_voltage())

        # Many valid solutions for passing this data along, dictionary is fine
        sample_data = {
            'timestamp': timestamp,
            'voltage': voltage_list
        }
        return sample_data


if __name__ == '__main__':
    sampler = Sampler()
    while True:
        sample = sampler.sample()
        print(sample)
        time.sleep(2)