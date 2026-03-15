# This program simulates the operation of a weather station's transformer.
# There is only one transformer per weather station,
# it is the central routing point for all data created by its sampler arrays.

import json
import time
import numpy as np
import requests
from sampler import Sampler


class Transformer:
    '''
    Transforms sampled voltage readings into weather values
    and sends them to the database through a REST API.
    '''


    def __init__(self, config_path='config.json'):
        config = self.load_config(config_path)
        transformer_config = config.get('transformer', {})

        # Runtime configuration loaded from JSON
        self.timeout = transformer_config.get('timeout')
        sampler_count = transformer_config.get('sampler_count')
        self.api_url = transformer_config.get('api_url')

        # Create samplers dynamically per config file
        self.sampler_list = []
        for _ in range(sampler_count):
            self.sampler_list.append(Sampler())

    def load_config(self, config_path):
        '''
        Helper used in the first line of __init__ to load configuration from a JSON file.
        '''
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f'Config file not found: {config_path}. Using defaults.')
            return {}
        except json.JSONDecodeError:
            print(f'Invalid JSON in config file: {config_path}. Using defaults.')
            return {}

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
                avg_ls.append(np.average(sample['voltage']))
            voltage = round(np.average(avg_ls), 2)
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