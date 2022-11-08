#! /usr/bin/env python3
"""
Runs Software-in-the-loop simulation with application
"""

# Project import
from src import CadenceTracker, ClassifierSM, DataQueue, TrajectoryLookUp
from utils import parse_mt_file
# Python import
import argparse
import os
import warnings
# 3rd-party import
from matplotlib import pyplot as plt


def sil_main(datafile, graph_title, params):
    # Parse Args
    data_rate = params.get('data_rate', 100) #Rate of IMU(Hz)
    dq_window = params.get('dq_window', 4) # time window of data queue

    csm_modelfile = params['modelfile'] # filepath to classifier model
    csm_threshold = params.get('threshold', .8) # threshold for accepting prediction
    csm_window = params.get('csm_window', 3.5) # time window of classifier wrapper

    ct_window = params.get('ct_window', 3.5) # time window of cadence tracker
    ct_method = params.get('ct_method', 'indirect')

    # Make Objects
    DQ = DataQueue(data_rate_Hz=data_rate, time_window_s=dq_window)
    ClassSM = ClassifierSM(csm_modelfile, threshold=csm_threshold, 
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
    #filepath = os.path.join('data',datafile)
    data_dict = parse_mt_file(datafile)

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
        DQ.append(accel_measure)
        datum = DQ.get_latest_entries(CT.TIME_WINDOW)
        if datum is not None:
            ClassSM.predict(datum, data_rate)
            if ClassSM.STATE == 'walking':
                CT.walking = True
            else:
                CT.walking = False
            CT.update_cadence(datum)
            if CT.steps_per_window != -1:
                tgt_angle = TLU.get_pos_setpoint(CT.steps_per_window, CT.TIME_WINDOW)
                print(f"angle {tgt_angle}")
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


def _check_threshold(arg):
    try:
        val = float(arg)
    except ValueError as err:
        raise argparse.ArgumentTypeError(str(err))
    
    if val < 0.0 or val >= 1.0:
        msg = f"Threshold must be between 0 and 1. Recieved {val}"
        raise argparse.ArgumentTypeError(msg)
    return val

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run software in the loop simulation')
    parser.add_argument('datafile', type=str, help="Log file of IMU data to test software with")
    parser.add_argument('modelfile', type=str, help="Model file of classifier to run with")
    parser.add_argument('-g', '--title', type=str, default="SIL Results", help="Graph title of SIL Results")
    parser.add_argument('-r', '--data_rate', type=int, default=100, 
        help="Sample rate of the logged data or incoming data rate of the IMU")
    parser.add_argument('-n', '--queue_window', type=float, default=4.0, 
        help="How many seconds of IMU data the queue should have in memory")
    parser.add_argument('-w', '--window', type=float, default=3.5,
        help="How many seconds of data should be considered for classification and cadence tracking")
    parser.add_argument('-t', '--threshold', type=_check_threshold, default=.8,
        help="Confidence threshold for classifier; must be between 0 and 1")
    parser.add_argument('-m', '--method', type=str, default='indirect', choices=['direct', 'indirect'],
        help="Choose which method for counting steps; 'direct' counts acceleration pulses \
            while 'indirect' estimates with frequency analysis")
    
    args = parser.parse_args()
    params = {'data_rate': args.data_rate,
              'dq_window': args.queue_window,
              'modelfile': args.modelfile,
              'threshold': args.threshold,
              'csm_window': args.window,
              'ct_window': args.window,
              'ct_method': args.method}

    sil_main(args.datafile, args.title, params)

