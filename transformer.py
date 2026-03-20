import numpy as np


class Transformer:
    '''
    Transforms sampled voltage readings into weather values
    and sends them to the database through a REST API.
    '''

    def __init__(self,  sampler_list):
        self.sampler_list = sampler_list

    def voltage_to_temperature(self, voltage):
        return round(voltage / 2, 2)

    def run(self):
        # Call .sample() on each sampler in the sampler list
        samples = []
        for sampler in self.sampler_list:
            samples.append(sampler.sample())

        # Find their average voltage, round it for db storage
        avg_ls = []
        for sample in samples:
            avg_ls.append(np.average(sample['voltage']))

        voltage = round(np.average(avg_ls), 2)

        # Calculate temperature from voltage (the whole point of the transformer)
        temperature = self.voltage_to_temperature(voltage)

        # Return to main program as a dict, which will later be stored as a row in the db
        data_dict = {
            'timestamp': samples[0]['timestamp'],
            'voltage': voltage,
            'temperature': temperature
        }
        return data_dict