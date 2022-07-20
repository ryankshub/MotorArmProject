#! /usr/bin/env python3
"""
Main file for demo
"""

# Project import
from cadence_tracker import CadenceTracker
from imu_interface import ImuInterface
# Python import
from collections import deque
# 3rd-party import


if __name__ == "__main__":
    operation_freq = 100
    cadence_queue = deque([], maxlen=operation_freq//2)
    # Create Cadence Tracker
    CT = CadenceTracker(freq_Hz=operation_freq, time_window_s=3, method='direct')

    # Create Imu_interface
    imu_itf = ImuInterface(read_rate_Hz=operation_freq)

    # Connect to Odrive

    # Main loop

