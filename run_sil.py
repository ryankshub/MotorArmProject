#! /usr/bin/env python3
"""
Runs Software-in-the-loop simulation with application
"""

# Project import
from src import CadenceTracker, ClassiferSM, DataQueue, TrajectoryLookUp
from utils import parse_mt_file
# Python import
import argparse
import os
# 3rd-party import
from matplotlib import pyplot as plt


def sil_main(datafile, graph_title, **kwargs):
    # Parse Args
    data_rate = kwargs.get('data_rate', 100) #Rate of IMU(Hz)
    dq_window = kwargs.get('dq_window', 4) # time window of data queue

    csm_modelfile = kwargs['modelfile'] # filepath to classifier model
    csm_threshold = kwargs.get('threshold', .8) # threshold for accepting prediction
    csm_window = kwargs.get('csm_window', 3.5) # time window of classifier wrapper

    ct_window = kwargs.get('ct_window', 3.5) # time window of cadence tracker
    ct_method = kwargs.get('ct_method', 'indirect')

    # Make Objects
    DQ = DataQueue(data_rate_Hz=data_rate, time_window=dq_window)
    ClassSM = ClassiferSM(csm_modelfile, threshold=csm_threshold, 
        time_window=csm_window)
    CT = CadenceTracker(data_rate_Hz=data_rate, time_window_s=ct_window,
        method=ct_method)

    # Create Trajectory Look-Up
    profiles = {0.8: 'data/template_data/08ms.csv',
                0.9: 'data/template_data/09ms.csv',
                1.0: 'data/template_data/10ms.csv',
                1.1: 'data/template_data/11ms.csv',
                1.2: 'data/template_data/12ms.csv',
                1.3: 'data/template_data/13ms.csv',
                1.4: 'data/template_data/14ms.csv'}
    TLU = TrajectoryLookUp(profiles=profiles)

    # Parse data file
    print(f"Data file: {datafile}")
    filepath = os.path.join('data',datafile)
    data_dict = parse_mt_file(filepath)

    # Get time and data measurement
    time_steps = data_dict["Time_s"]
    accel_measures = data_dict["AccM"]

    #Execution Loop
    log_angle = []
    log_target = []
    log_steps = []
    log_time = []
    log_speeds = []
    for i in range(len(time_steps)):
        log_time.append(i)
        #Get measurements
        accel_measure = accel_measures[i]
        print(accel_measure)



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

