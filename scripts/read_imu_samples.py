#! /usr/bin/env python3

# Project import

# Python import
import time
# 3rd party imports
import matplotlib.pyplot as plt 
import numpy as np
import serial

ser = serial.Serial('/dev/ttyACM0',115200)
print('Talking to pico: ')
print(ser.name)

read_samples = 30 # anything bigger than 1 to start out

time_arr = []
while read_samples > 0:
    time_arr.append(time.time())
    data_read = ser.read_until(b'\n') # get the data as bytes
    print(data_read)
    data_text = str(data_read,'utf-8') # turn the bytes to a string
    data = [float(i) for i in data_text.split()] # turn the string into a list of floats

    read_samples -= 1
ser.close()

print('Data collection complete')
time_arr = np.array(time_arr)
time_diff = time_arr[1:] - time_arr[:-1]
time_log = time_arr - time_arr[0]
print(f"Mean time diff {time_diff.mean()}")
print(time_arr)
print(time_diff)
print(time_log)


