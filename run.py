from time import sleep
import json
import requests
from sampler import Sampler
from transformer import Transformer



def load_config(config_path='config.json'):
    # Loads a hardcoded config file, its contents dictates the behavior of the entire system
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Config file not found at {config_path}. Exiting...')
        exit(1)
    except json.JSONDecodeError:
        print(f'Invalid JSON in config file: {config_path}. Exiting...')
        exit(1)

def send_to_rest_api(api_url, data):
    # Make a post request to append data to the db using the rest api
    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        print('Data stored:', response.json())
    except requests.exceptions.RequestException as e:
        print('Failed to send:', e)

def main():
    # Read the config file, this will dictate how the program behaves
    config = load_config().get('station', {})
    # Retrieve variables from the config file to use as arguments 
    timeout = config.get('timeout')
    api_url = config.get('api_url')
    sampler_count = config.get('count')
    sensors_per_sampler = config.get('sensors_per_sampler')

    # Create objects: sensors, samplers, and a single transformer
    sampler_list = []
    for _ in range(sampler_count):
            sampler_list.append(Sampler(num_sensors=sensors_per_sampler))
    transformer = Transformer(sampler_list)

    # Begin the main loop, it will continue until interrupted by the user
    print('Starting weather station pipeline...')
    while True:
        data_dict = transformer.run()
        send_to_rest_api(api_url, data_dict)
        sleep(timeout)

if __name__ == '__main__':
    main()