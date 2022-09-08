#! /usr/bin/env python3
"""
Runs Hardware-in-the-loop simulation with application
"""

# Project import
from src import CadenceTracker, TrajectoryLookUp
from utils import parse_mt_file
# Python import
import argparse
import os
import time
# 3rd-party import
from matplotlib import pyplot as plt
import numpy as np
import odrive
from odrive.enums import *
import pandas as pd

def hil_main(datafile, operation_freq=100, time_window_s=4):
    print(f"Data file: {datafile}")
    # Parse data file
    filepath = os.path.join('data',datafile)
    data_dict = parse_mt_file(filepath)

    # Get time and data measurement
    time_steps = data_dict["Time_s"]
    accel_measures = data_dict["AccM"]

    # Create Cadence Tracker
    CT = CadenceTracker(freq_Hz=operation_freq, time_window_s=time_window_s, method='direct')

    # Create Trajectory Look-Up
    profiles = {0.8: 'data/template_data/08ms.csv',
                0.9: 'data/template_data/09ms.csv',
                1.0: 'data/template_data/10ms.csv',
                1.1: 'data/template_data/11ms.csv',
                1.2: 'data/template_data/12ms.csv',
                1.3: 'data/template_data/13ms.csv',
                1.4: 'data/template_data/14ms.csv'}

    traj_dict = TrajectoryLookUp(profiles=profiles)

    # Connect to Odrive
    # print("Finding the ODrive arm...")
    # odrv0 = odrive.find_any()
    # print("Found Odrive!!")
    # odrv0.axis0.requested_state = AXIS_STATE_IDLE
    # time.sleep(1)

    # Reset encoder to 0
    # odrv0.axis0.encoder.set_linear_count(0)

    # Configure Position Control
    # odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    # odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
    # odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    
    #Execution Loop
    encoder_df = pd.read_csv('data/template_data/10ms.csv', names=["Position","Torque"])
    traj_dict.angle = 0.0
    count = 0
    log_angle = []
    log_steps = []
    log_time = []
    log_speeds = []
    for i in range(len(time_steps)):
        log_time.append(i)
        #Get measurements
        accel_measure = accel_measures[i]
        # encoder_measure = odrv0.axis0.encoder.pos_estimate

        # Apply measurements to cadence tracker
        CT.add_measurement(accel_measure)
        # traj_dict.angle = encoder_measure
        # Pass cadence to trajectory look-up
        steps = CT.calculate_cadence()
        log_steps.append(steps)
        if (steps > 0): # Presume walking
            pos_setpoint = traj_dict.get_pos_setpoint(steps, time_window_s)
            log_angle.append(pos_setpoint)
            log_speeds.append(traj_dict._fast_speed)
            print(f"Slow speed: {traj_dict._slow_speed}, Fast speed: {traj_dict._fast_speed}")        
            traj_dict.angle = pos_setpoint ### TODO: REMOVE; JUST FOR DEBUGGING
        else:
            log_angle.append(traj_dict.angle)
            log_speeds.append(0)
        # odrv0.axis0.controller.input_pos = pos_setpoint

    plot_hil_results(log_time, log_angle, log_steps, log_speeds)
    return 0


def plot_hil_results(times, angles, steps, speeds):
    """
    Plot Hil results
    """

    fig, axs = plt.subplots(3, 1, sharex=True)
    fig.suptitle("Software HIL with 'direct' Cadence Tracker for Walk 1.0m/s")
    axs[0].set_title("Target angle by Trajectory Look-Up")
    axs[0].plot(times, angles, label="target angle", color='b')
    #axs[0].set_xlabel("Time [sec]")
    axs[0].set_ylabel("Target angle [rev]")

    axs[1].set_title("Estimated steps taken in past time window")
    axs[1].plot(times, steps, label="estimated steps", color="g")
    #axs[1].set_xlabel("Time [sec]")
    axs[1].set_ylabel("Steps")

    axs[2].set_title("Estimated walking speed (based on RKS model)")
    axs[2].plot(times, speeds, label="Target Speed", color='r')
    axs[2].set_xlabel("Time [msec]")
    axs[2].set_ylabel("Estimated Walking Speed [m/s]")

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Hardware in the loop simulation')
    parser.add_argument('datafile', type=str, help="Log file of IMU data to run the arm with")
    args = parser.parse_args()
    hil_main(args.datafile)
