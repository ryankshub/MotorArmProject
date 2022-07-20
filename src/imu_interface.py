#! /usr/bin/env python3
"""
File for IMU Interface class which manages serial communication 
with Raspberry pico. 
"""

# Python Import
from time import sleep
# Project Import

# 3rd-Party Import
import serial

class ImuInterface:
    """
    Read data from MPU6050 via a Raspberry pi pico
    """
    def __init__(self, read_rate_Hz=100, port='/dev/ttyACM0', baudrate=115200):
        """
        Constructor for the MPU6050

        int read_rate_hz - Frequency to read data; default 100Hz
        string port - Serial port for the device; default /dev/ttyACM0
        int baudrate - bits per second; default 115200
        """
        self._ser = serial.Serial(port, baudrate)
        self._sleep_time = 1/read_rate_Hz
        print(f'Talking to pico: {self._ser}')


    def read(self):
        """
        Read and return IMU data

        Rtn:
        6 list array with:
        [acceleration x, y, z, gyroscope x, y, z]
        """
        data_read = self._ser.read_until(b'\n') # get the data as bytes
        data_text = str(data_read,'utf-8') # turn the bytes to a string
        data = [float(i) for i in data_text.split()] # turn the string into a list of floats
        sleep(self._sleep_time)
        return data


    def close(self):
        """
        Close serial port
        """
        self._ser.close()
        self._ser = None

    
