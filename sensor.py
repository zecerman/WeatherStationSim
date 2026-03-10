# This program simulates the operation of a weather station's sensor, per spec:
# The Sensor is the first component in the Weather Station Pipeline.
# It continuously produces voltage readings that are later sampled, transformed, and stored.

import random as r
import time

class Sensor:
    '''
    Allows for sensor objects to be initialized
    Simulates a physical sensor producing voltage readings.
    '''

    def read_voltage(self):
        '''Generate a simulated voltage reading.'''
        voltage = voltage = r.randint(100, 150)
        return voltage

if __name__ == '__main__':
    sensor = Sensor()

    while True:
        voltage = sensor.read_voltage()
        print(f'Sensor Voltage: {voltage} V')
        time.sleep(1)

