# This program simulates the operation of a weather station's transformer.
# There is only one transformer per weather station,
# it is the central routing point for all data created by its sampler arrays.

import time
import numpy as np
import requests
import sys
from sampler import Sampler


class Transformer:
    '''
    Transforms sampled voltage readings into weather values
    and sends them to the database through a REST API.
    '''

    def __init__(self):
        # Use command line arguments to determine sampling rate
        self.timeout = int(sys.argv[1])
        # TODO 2 samplers per transformer is currently hard coded, 
        # could easily be changed to a dynamic number
        self.sampler_list = []
        for _ in range(2):
            self.sampler_list.append(Sampler())
        # Port for REST_API is arbitrary, hard coding it is fine
        self.api_url = 'http://127.0.0.1:5000/weather'

    def voltage_to_temperature(self, voltage):
        convert_to_fahrenheit = 2
        temperature = voltage / convert_to_fahrenheit
        return round(temperature, 2)

    def voltage_to_precipitation(self, voltage):
        convert_to_clouds = 300
        precipitation = voltage / convert_to_clouds
        return round(precipitation, 2)

    def send_to_rest_api(self, data):
        '''
        Send transformed data to the REST API as JSON.
        '''
        try:
            response = requests.post(self.api_url, json=data, timeout=5)
            response.raise_for_status()
            print('Data stored successfully:', response.json())
        except requests.exceptions.RequestException as e:
            print('Failed to send data to REST API:', e)

    def run(self):
        '''
        Run the (transformer -> REST API -> database) pipeline continuously.
        '''
        while True:
            samples = []
            # Get samples from all samplers which are assocaited with this tower
            for sampler in self.sampler_list:
                samples.append(sampler.sample())
            # Extract the average voltage from each sensor array which responded
            avg_ls = []
            for sample in samples:
                avg_ls = np.average(sample['voltage'])
            voltage = np.average(avg_ls)
            # Make some calculations with this value
            t = self.voltage_to_temperature(voltage)
            p = self.voltage_to_precipitation(voltage)
            # Format our data into a JSON friendly format
            transformed_data = {
                'timestamp': samples[0]['timestamp'],
                'voltage': voltage,
                'temperature': t,
                'precipitation': p
            }
            # Save to db using rest api
            self.send_to_rest_api(transformed_data)
            time.sleep(self.timeout)


if __name__ == '__main__':
    transformer = Transformer()
    transformer.run()