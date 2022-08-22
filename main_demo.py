#! /usr/bin/env python3
"""
Main file for demo
"""

# Project import
from cadence_tracker import CadenceTracker
from imu_interface import ImuInterface
# Python import
from time import sleep
# 3rd-party import
import numpy as np
import odrive
from odrive.enums import *


if __name__ == "__main__":
    operation_freq = 100
    # Create Cadence Tracker
    CT = CadenceTracker(freq_Hz=operation_freq, time_window_s=4, method='indirect')

    # Create Imu_interface
    imu_itf = ImuInterface(read_rate_Hz=operation_freq)

    # Connect to Odrive
    print("Finding the ODrive arm...")
    odrv0 = odrive.find_any()
    print("Found Odrive!!")
    odrv0.axis0.requested_state = AXIS_STATE_IDLE
    sleep(1)
    # Reset encoder to 0
    odrv0.axis0.encoder.set_linear_count(0)

    # Calculate limit
    lower_limit = 0.0
    upper_limit = -CT._DEGREES_PER_STEP/360.0
    swing_forward = True

    # Configure Velocity control
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    # Main loop
    count = 0
    while(count < 5000):
        count += 1
        #sleep(.01)
        measurement = imu_itf.read()
        accel_val = np.sqrt(np.power(measurement[0], 2) 
            + np.power(measurement[1], 2) + np.power(measurement[2], 2))
        CT.add_measurement(accel_val)
        cadence = (CT.calculate_cadence())/360.0

        if (swing_forward):
            cadence *= -1

        # Set Cadence
        odrv0.axis0.controller.input_vel = cadence
        print(f"Cadence: {cadence}")
        # Check angle
        encoder_angle = odrv0.axis0.encoder.pos_estimate
        #print(f"Encoder angle: {encoder_angle}")
        if (encoder_angle < upper_limit):
            swing_forward = False
        elif (encoder_angle > lower_limit):
            swing_forward = True
    
    #Stop the arm
    odrv0.axis0.requested_state = AXIS_STATE_IDLE
    


