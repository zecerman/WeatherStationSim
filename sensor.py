# This program simulates the operation of a weather station's sensor, per spec:
# The Sensor is the first component in the Weather Station Pipeline.
# It continuously produces voltage readings that are later sampled, transformed, and stored.

# Import dependancies
import random as r
import time

# Expose the sensor object
def sensor_object(altitude, sampling_rate):
    # For as long as the sensor object is being called:
    while (True):
        # The sensor will read a voltage (which is a function of altitude)
        voltage = r.randint(80, 140) * altitude 
        # It records that voltage in its datastream
        print(voltage)
        # It waits based on its specified sampling time
        time.sleep(sampling_rate)

# Dummy main method TODO
sensor_object(1,1)
