#! /usr/bin/env python3

#Python imports
import argparse
import os
import sys

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project import
from utils import 

# 3rd party imports
import pandas as pd
import serial

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log IMU data into simple file")
    parser.add_argument("port", type=str, help="device port for IMU connection")
    parser.add_argument("logfile", type=str, help="filepath of newly created logfile")
    parser.add_argument("-a", "--action", type=str, default='walking', help="Activity \
        being recorded.")
    parser.add_argument("-b", "--baudrate", type=int, default=115200, 
        help="baudrate of the connection")
    parser.add_argument("-t", "--time", type=float, default=5.0, help="Length of logfile\
        (in seconds)")

    args = parser.parse_args()

    ser = serial.Serial(args.port, args.baudrate)
    print(f"Talking to {ser.name}")
    frame = 1
    accx = []
    accy = []
    accz = []
    input("Hit Enter to start logging")
    while(frame < 501):
        data_read = ser.read_until(b'\n')
        data_text = str(data_read, 'utf-8')
        ax, ay, az, _, _, _ = [float(i) for i in data_text.split()]
        accx.append(ax)
        accy.append(ay)
        accz.append(az)
        frame += 1
    print("Done reading")
    df = pd.DataFrame()
    df['Frames#'] = [i for i in range(1,501)]
    df['Time'] = [(.01*(i-1)) for i in df['Frames#']]
    df['AccX'] = accx
    df['AccY'] = accy
    df['AccZ'] = accz

    create_simple_file(args.logfile, args.action, 100.0, df)