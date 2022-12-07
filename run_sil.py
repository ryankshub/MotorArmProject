#! /usr/bin/env python3
"""
Runs Software-in-the-loop simulation with application
"""

# Project import
from src import CadenceTracker, ClassifierSM, DataQueue, \
    PendulumGUI, TrajectoryLookUp
from utils import parse_mt_file, read_imu
# Python import
import argparse
import os
import time
# 3rd-party import
from matplotlib import pyplot as plt
import numpy as np
import serial


def object_setup(params):
    """
    """
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

    return DQ, ClassSM, CT, TLU


def exe_loop(accel_measure, data_rate, DQ, ClassSM, CT, TLU, logger_dict, 
    state, step_count, time_step = -1):
    """
    Main execution loop

    Args:
        float accel_measure - incoming acceleration magnitude reading
        float data_rate - data_rate(Hz) of incoming data
        DataQueue DQ - main data queue holding incoming data
        ClassifierSM ClassSM - Acitivity classifier
        CadenceTracker CT - determines when a step has taken place and
            tracks the cadence of the user
        Trajectory Look-up - Look-up table of possible arm trajectories
            the system could follow
        dict logger_dict - Dictionary to log state and step_count
        TODO: Remove
        string state - current activity being performed
        int step_count - number of steps taken during run
    """
    # Add latest data to queue
    DQ.append(accel_measure)
    # Grab the latest elements from queue
    datum = DQ.get_latest_entries(CT.TIME_WINDOW)

    if datum is not None:
        # Predict which activity is being performed
        ClassSM.predict(datum, data_rate)
        if ClassSM.STATE == 'walking':
            CT.walking = True
        else:
            CT.walking = False

        # Update cadence
        CT.update_cadence(datum)

        # Update target angle
        tgt_angle = TLU.get_pos_setpoint(CT.steps_per_window, CT.TIME_WINDOW)

        #TODO: DEBUGGING: Add GUI HOOKS
        if (state != ClassSM.STATE):
            print(f"STATE: {ClassSM.STATE}")
            state = ClassSM.STATE
        if (step_count != CT.step_count):
            print(f"TIME: {time_step}, STEP COUNT: {CT.step_count}")
            print(f"SPW {CT.steps_per_window}")
            step_count = CT.step_count
        
        logger_dict["logstates"].append(ClassSM.STATE)
        logger_dict["steps"].append(CT.step_count)

        return tgt_angle, state, CT.step_count
    else:
        logger_dict["logstates"].append("booting_up")
        logger_dict["steps"].append(0)
        return TLU.angle, state, CT.step_count


def sil_main(datafile, graph_title, params):
    # Set objects
    DQ, ClassSM, CT, TLU = object_setup(params)

    # Get input rate
    data_rate = params.get('data_rate', 100)

    # Parse data file
    print(f"Data file: {datafile}")
    #filepath = os.path.join('data',datafile)
    data_dict = parse_mt_file(datafile)

    # Get time and data measurement
    time_steps = data_dict["Time_s"]
    accel_measures = data_dict["AccM"]

    # Make return log for playback
    logger_dict = {"logname": os.path.basename(datafile),
                   "logstates": [],
                   "theta1": [],
                   "steps": []}

    #Execution Loop
    state = 'unknown'
    step_count = 0
    for i in range(len(time_steps)):
        #Get measurements
        accel_measure = accel_measures[i]
        tgt_angle, state, step_count = exe_loop(accel_measure, data_rate, DQ, 
                                                ClassSM, CT, TLU, logger_dict,
                                                state, step_count, 
                                                time_steps[i])
        # TODO Add simple noise model to represent encoder precision
        TLU.angle = tgt_angle
        logger_dict["theta1"].append(tgt_angle*2*np.pi)
    
    return logger_dict


def live_sil_main(port, params, baudrate=115200):
    # Set objects
    DQ, ClassSM, CT, TLU = object_setup(params)

    # Get input rate
    data_rate = params.get('data_rate', 100)

    # Set up serial port
    ser = serial.Serial(port, baudrate)

    # Get time limit
    time_limit = params.get('time_limit', 30.0)

    # Read IMU
    state = 'unknown'
    step_count = 0
    angles_log = []
    infinite_loop = time_limit < 0
    start_time = time.time()
    while(infinite_loop | time.time() - start_time < time_limit):
        ax, ay, az = read_imu(ser)
        accel_measure = np.sqrt(
            np.sum( np.power([float(ax), float(ay), float(az)], 2) ) 
            )
        tgt_angle, state, step_count = exe_loop(accel_measure, data_rate, DQ, 
                                                ClassSM, CT, TLU, state, 
                                                step_count)
        # TODO Add simple noise model to represent encoder precision
        TLU.angle = tgt_angle
        angles_log.append(tgt_angle*2*np.pi)
    
    ser.close()

    return angles_log


def _check_threshold(arg):
    """
    Argument parsing fcn that checks if the classifier threshold is in the 
    range (0,1]
    """
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
    parser.add_argument('imu_source', type=str, help="Source of IMU data to test software with. \
        use --port arg to specify IMU port, else use filepath to logfile")
    parser.add_argument('modelfile', type=str, help="Model file of classifier to run with")
    parser.add_argument('-g', '--title', type=str, default="SIL Results", help="Graph title of SIL Results")
    parser.add_argument('-r', '--data_rate', type=int, default=100, 
        help="Sample rate of the logged data or incoming data rate of the IMU")
    parser.add_argument('-n', '--queue_window', type=float, default=4.0, 
        help="How many seconds of IMU data the queue should have in memory")
    parser.add_argument('-w', '--window', type=float, default=3.5,
        help="How many seconds of data should be considered for classification and cadence tracking")
    parser.add_argument('-c', '--threshold', type=_check_threshold, default=.8,
        help="Confidence threshold for classifier; must be between 0 and 1")
    parser.add_argument('-m', '--method', type=str, default='indirect', choices=['direct', 'indirect'],
        help="Choose which method for counting steps; 'direct' counts acceleration pulses \
            while 'indirect' estimates with frequency analysis")
    parser.add_argument('-p', '--port', action='store_true', help="Port to connect to the IMU")
    parser.add_argument("-t", "--time_limit", type=float, default=30.0, 
        help="Only applies to live run, time_limit of the run. For an endless\
             run, set time_limit negative")
    
    args = parser.parse_args()
    params = {'data_rate': args.data_rate,
              'dq_window': args.queue_window,
              'modelfile': args.modelfile,
              'threshold': args.threshold,
              'csm_window': args.window,
              'ct_window': args.window,
              'ct_method': args.method,
              'time_limit': args.time_limit}
    

    if args.port:
        # live operation 
        logger_dict = live_sil_main(args.imu_source, params)
    else:
        # playback from logfile
        logger_dict = sil_main(args.imu_source, args.title, params)
    
    app = PendulumGUI(False)
    app.run_playback(logger_dict, 50)