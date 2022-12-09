#! /usr/bin/env python3
"""
Runs Software-in-the-loop simulation with application
"""

# Project import
from src import CadenceTracker, ClassifierSM, DataQueue, \
    PendulumGUI, TrajectoryLookUp, TrajectorySplineGenerator
from utils import parse_mt_file, read_imu
# Python import
import argparse
from collections import deque
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
    ct_method = params.get('ct_method', 'direct')

    double_pend = params.get('double_pend', False) 
    # Make Objects
    DQ = DataQueue(data_rate_Hz=data_rate, time_window_s=dq_window)
    ClassSM = ClassifierSM(csm_modelfile, threshold=csm_threshold, 
        time_window=csm_window)
    CT = CadenceTracker(data_rate_Hz=data_rate, time_window_s=ct_window,
        method=ct_method)

    if params.get('use_look', False):
        # Create Trajectory Look-Up
        profiles = {0.8: 'data/template_data/08ms.csv',
                    0.9: 'data/template_data/09ms.csv',
                    1.0: 'data/template_data/10ms.csv',
                    1.1: 'data/template_data/11ms.csv',
                    1.2: 'data/template_data/12ms.csv',
                    1.3: 'data/template_data/13ms.csv',
                    1.4: 'data/template_data/14ms.csv'}
        TRAJ = TrajectoryLookUp(profiles=profiles)
    else:
        TRAJ = TrajectorySplineGenerator(sample_rate=data_rate, 
                                         double_pend=double_pend)

    return DQ, ClassSM, CT, TRAJ


def exe_loop(accel_measure, data_rate, DQ, ClassSM, CT, TRAJ, logger_dict, 
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
        el_angle, sh_angle = TRAJ.get_pos_setpoint(CT.steps_per_window, 
                                                   CT.TIME_WINDOW,
                                                   CT.time_till_step)

        #TODO: DEBUGGING: Add GUI HOOKS
        if (state != ClassSM.STATE):
            print(f"STATE: {ClassSM.STATE}")
            state = ClassSM.STATE
        if (step_count != CT.step_count):
            print(f"TIME: {time_step}, STEP COUNT: {CT.step_count}, " 
                f"SPW {CT.steps_per_window}")
        
        logger_dict["logstates"].append(ClassSM.STATE)
        logger_dict["steps"].append(CT.step_count)

        return el_angle, sh_angle, state, CT.step_count
    else:
        logger_dict["logstates"].append("booting_up")
        logger_dict["steps"].append(0)
        return TRAJ.angle, TRAJ.sh_angle, state, CT.step_count


def sil_main(datafile, graph_title, params):
    # Set objects
    DQ, ClassSM, CT, TRAJ = object_setup(params)

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
    if params.get("double_pend", False):
        logger_dict["theta2"] = []

    #Execution Loop
    state = 'unknown'
    step_count = 0
    for i in range(len(time_steps)):
        #Get measurements
        accel_measure = accel_measures[i]
        el_angle, sh_angle, state, step_count = exe_loop(accel_measure, data_rate, DQ, 
                                                ClassSM, CT, TRAJ, logger_dict,
                                                state, step_count, 
                                                time_steps[i])
        # TODO Add simple noise model to represent encoder precision
        TRAJ.angle = el_angle
        TRAJ.sh_angle = sh_angle
        if sh_angle is None:
            logger_dict["theta1"].append(el_angle*2*np.pi)
        else:
            logger_dict["theta1"].append(sh_angle*2*np.pi)
            logger_dict["theta2"].append(el_angle*2*np.pi)

    return logger_dict


def live_sil_main(port, params, baudrate=115200, gui_update_fcn=None):
    # Set objects
    DQ, ClassSM, CT, TRAJ = object_setup(params)

    # Get input rate
    data_rate = params.get('data_rate', 100)

    # Set up serial port
    ser = serial.Serial(port, baudrate)

    # Get time limit
    time_limit = params.get('time_limit', 30.0)

    # Logger dict for playback
    logger_dict = {"logname": "Live!",
                    "logstates": deque(),
                    "theta1": deque(),
                    "steps": deque()}
    if params.get("double_pend", False):
        logger_dict["theta2"] = deque()

    # Read IMU
    state = 'unknown'
    step_count = 0
    infinite_loop = time_limit < 0
    start_time = time.time()
    running = True
    while(infinite_loop | (time.time() - start_time < time_limit) \
        and running):
        ax, ay, az = read_imu(ser)
        accel_measure = np.sqrt(
            np.sum( np.power([float(ax), float(ay), float(az)], 2) ) 
            )
        el_angle, sh_angle, state, step_count = exe_loop(accel_measure, data_rate, DQ, 
                                                ClassSM, CT, TRAJ, logger_dict,
                                                state, step_count)
        # TODO Add simple noise model to represent encoder precision
        TRAJ.angle = el_angle
        TRAJ.sh_angle = sh_angle
        
        #Update Gui
        if not params.get('headless', False):      
            if sh_angle is None:
                running = gui_update_fcn(ClassSM.STATE, 
                                         CT.step_count, 
                                         el_angle*2*np.pi)
            else:
                running = gui_update_fcn(ClassSM.STATE, 
                                         CT.step_count, 
                                         sh_angle*2*np.pi, 
                                         el_angle*2*np.pi)
    ser.close()


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
    parser.add_argument('data_source', type=str, help="Source of accel data to test software with. \
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
    parser.add_argument("-l", "--look_up", action='store_true', 
        help="Flag in order to use the trajectory look-up table instead of the\
            trajectory spline generator")
    parser.add_argument("-d", "--double_pend", action='store_true', 
        help="Use the double pendulum model. This can only be used with \
            trajectory spline generator (the look_up option is ignored")
    parser.add_argument("-i", "--headless", action='store_true', 
        help="Run the live sil without gui")
    
    args = parser.parse_args()
    params = {'data_rate': args.data_rate,
              'dq_window': args.queue_window,
              'modelfile': args.modelfile,
              'threshold': args.threshold,
              'csm_window': args.window,
              'ct_window': args.window,
              'ct_method': args.method,
              'time_limit': args.time_limit,
              'use_lookup': args.look_up and (not args.double_pend),
              "double_pend": args.double_pend,
              "headless": args.headless}
    

    if args.port:
        # live operation
        if args.headless:
            live_sil_main(args.data_source, params)
        else:
            app = PendulumGUI(double_pend=args.double_pend, live=True)
            app.setup_live()
            live_sil_main(args.data_source, params, gui_update_fcn=app.live_update)
            app.await_death()
    else:
        # playback from logfile
        logger_dict = sil_main(args.data_source, args.title, params)
        app = PendulumGUI(double_pend=args.double_pend)
        app.run_playback(logger_dict)