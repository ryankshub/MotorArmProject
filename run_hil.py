#! /usr/bin/env python3
"""
Runs Hardware-in-the-loop simulation with application
"""

# Project import
from src import CadenceTracker, ImuInterface, TrajectoryLookUp
from utils import parse_mt_file
# Python import
import argparse

# 3rd-party import
import numpy as np
import odrive
from odrive.enums import *

def hil_main(datafile, opertion_freq=100, time_window_s=4):
    print(f"Data file: {datafile}")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Hardware in the loop simulation')
    parser.add_argument('datafile', type=str, help="Log file of IMU data to run the arm with")
    args = parser.parse_args()
    hil_main(args.datafile)
