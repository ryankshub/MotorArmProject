#! /usr/bin/env python3

# Project import

# Python import

# 3rd party imports
import matplotlib.pyplot as plt 
import serial

ser = serial.Serial('/dev/ttyACM0',115200)
print('Talking to pico: ')
print(ser.name)

read_samples = 20 # anything bigger than 1 to start out
ax = []
ay = []
az = []
gx = []
gy = []
gz = []

while read_samples > 0:
    data_read = ser.read_until(b'\n') # get the data as bytes
    print(data_read)
    data_text = str(data_read,'utf-8') # turn the bytes to a string
    data = [float(i) for i in data_text.split()] # turn the string into a list of floats

    ax.append(data[0])
    ay.append(data[1])
    az.append(data[2])
    gx.append(data[3])
    gy.append(data[4])
    gz.append(data[5])

    read_samples -= 1
ser.close()

print('Data collection complete')


