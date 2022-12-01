#! /usr/bin/env python3

# Python import
import os
import sys
import time

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project import
from utils import read_imu

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
    data = read_imu(ser, debug=True)
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


