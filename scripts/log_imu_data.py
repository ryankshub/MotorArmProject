#! /usr/bin/env python3

#Python imports
import argparse
import os
import sys
import time

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project import
from utils import create_simple_file

# 3rd party imports
import pandas as pd
import serial

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log IMU data into simple \
        file")
    parser.add_argument("port", type=str, help="device port for IMU \
        connection")
    parser.add_argument("logfile", type=str, help="filepath of newly created \
        logfile")
    parser.add_argument("-a", "--action", type=str, default='walking', 
        help="Activity being recorded.")
    parser.add_argument("-b", "--baudrate", type=int, default=115200, 
        help="baudrate of the connection")
    parser.add_argument("-t", "--time_limit", type=float, default=5.0, 
        help="Length of logfile (in seconds)")
    parser.add_argument("-s", "--sample_rate", type=float, default=100.0, 
        help="Sample rate of the IMU I2C interface")

    args = parser.parse_args()
    #Log data
    frame = 1
    time_arr = []
    accx = []
    accy = []
    accz = []
    time_limit = args.time_limit - (1/args.sample_rate)
    input("Hit Enter to start logging")

    ser = serial.Serial(args.port, args.baudrate)
    print(f"Talking to {ser.name}")
    start_time = time.time()
    time_diff = 0

    while(time_diff < time_limit):
        time_diff = time.time() - start_time
        time_arr.append(time_diff)
        data_read = ser.read_until(b'\n')
        print(data_read)
        data_text = str(data_read, 'utf-8')
        ax, ay, az = [float(i) for i in data_text.split()]
        accx.append(ax)
        accy.append(ay)
        accz.append(az)
        frame += 1

    ser.close()
    print("Done reading")
    df = pd.DataFrame()
    df['Frames#'] = [i for i in range(1, frame)]
    df['Time'] = time_arr
    df['AccX'] = accx
    df['AccY'] = accy
    df['AccZ'] = accz

    create_simple_file(args.logfile, args.action, args.sample_rate, df)
    print(f"File {args.logfile} is created")