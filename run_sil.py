#! /usr/bin/env python3
"""
Runs Software-in-the-loop simulation with application
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
import pandas as pd

def sil_main(datafile, graph_title, operation_freq=100, time_window_s=4):
    #TODO Fix this for SIL operation
    print(f"Data file: {datafile}")
    # Parse data file
    filepath = os.path.join('data',datafile)
    data_dict = parse_mt_file(filepath)

    # Get time and data measurement
    time_steps = data_dict["Time_s"]
    accel_measures = data_dict["AccM"]

    # Create Cadence Tracker
    CT = CadenceTracker(freq_Hz=operation_freq, time_window_s=time_window_s, method='indirect')

    # Create Trajectory Look-Up
    profiles = {0.8: 'data/template_data/08ms.csv',
                0.9: 'data/template_data/09ms.csv',
                1.0: 'data/template_data/10ms.csv',
                1.1: 'data/template_data/11ms.csv',
                1.2: 'data/template_data/12ms.csv',
                1.3: 'data/template_data/13ms.csv',
                1.4: 'data/template_data/14ms.csv'}

    traj_dict = TrajectoryLookUp(profiles=profiles)
    
    #Execution Loop
    traj_dict.angle = 0.0
    log_angle = []
    log_target = []
    log_steps = []
    log_time = []
    log_speeds = []
    for i in range(len(time_steps)):
        log_time.append(i)
        #Get measurements
        accel_measure = accel_measures[i]
        encoder_measure = odrv0.axis0.encoder.pos_estimate

        # Apply measurements to cadence tracker
        CT.add_measurement(accel_measure)
        traj_dict.angle = encoder_measure
        # Pass cadence to trajectory look-up
        steps = CT.calculate_cadence()
        log_steps.append(steps)
        if (steps > 0): # Presume walking
            pos_setpoint = traj_dict.get_pos_setpoint(steps, time_window_s)
            log_angle.append(pos_setpoint)
            log_speeds.append(traj_dict._fast_speed)
            print(f"Slow speed: {traj_dict._slow_speed}, Fast speed: {traj_dict._fast_speed}")
            odrv0.axis0.controller.input_pos = pos_setpoint        
            #traj_dict.angle = pos_setpoint ### TODO: REMOVE; JUST FOR DEBUGGING
        else:
            log_angle.append(traj_dict.angle)
            log_speeds.append(0)

    plot_sil_results(graph_title, log_time, log_angle, log_target, log_steps, log_speeds)
    return 0


def plot_sil_results(title, times, angles, targets, steps, speeds):
    """
    Plot Hil results
    """

    fig, axs = plt.subplots(3, 1, sharex=True)
    fig.suptitle(title)
    axs[0].set_title("Target angle vs Encoder angle by Trajectory Look-Up")
    axs[0].plot(times, targets, label="target angle", color='b')
    axs[0].plot(times, angles, label="encoder angle", color='k')
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
    parser.add_argument('-t', '--title', type=str, default="SIL Results", help="Graph title of SIL Results")
    args = parser.parse_args()
    sil_main(args.datafile, args.title)

