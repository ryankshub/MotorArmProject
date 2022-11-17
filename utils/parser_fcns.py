#! /usr/bin/env python3
"""
Collection of parsers for the various data files in project
"""

# Project import

# Python import
import csv
import datetime

# 3rd-party import
import numpy as np
import pandas as pd

def parse_mt_file(filepath, ACTION_LINE = 4, RATE_LINE = 5):
    """
    Parse a data file from MT IMU Software. 

    Args:
        string - filepath: filepath to MT .txt file
        int - ACTION_LINE: A const value to represent which fileline
            has the action being performed
        int - RATE_LINE: A const value representing which fileline
            has the sample rate (in Hz) of the data collected.
    
    Return:
        dict with the following:
            'Time_s': timestamp array in seconds
            'AccX': Array of accelerations along the X-axis(this typically points forward) in m/s/s
            'AccY': Array of accelerations along the Y-axis(this typically point downward) in m/s/s
            'AccZ': Array of accelerations along the Z-axis(this typically points leftward) in m/s/s
            'AccM': Array of magnitude acceleration
            'FreeAccX': Same as 'AccX' without the effect of gravity
            'FreeAccY': Same as 'AccY' without the effect of gravity
            'FreeAccZ': Same as 'AccZ' without the effect of gravity
            'Action': Activity being logged (eg 'walking', 'squating', etc)
            'SampleRate': Rate of data collection[in Hz]
    """
    df = pd.read_csv(filepath, skiprows=6)
    # Output data rate is 100Hz or 0.01s between samples
    start_sample = df['PacketCounter'][0]
    df['Time_s'] = [0.01 * (df['PacketCounter'][i] - start_sample) for i in range(len(df['PacketCounter']))]
    df['AccM'] = [np.sqrt(np.power(df['Acc_X'][i], 2) + np.power(df['Acc_Y'][i], 2) + np.power(df['Acc_Z'][i], 2))
                    for i in range(len(df['Acc_X']))]
    rtn_dic = {'Time_s': df['Time_s'].values,
               'AccX': df['Acc_X'].values,
               'AccY': df['Acc_Y'].values,
               'AccZ': df['Acc_Z'].values,
               'AccM': df['AccM'].values,
               'FreeAccX': df['FreeAcc_X'].values,
               'FreeAccY': df['FreeAcc_Y'].values,
               'FreeAccZ': df['FreeAcc_Z'].values}

    with open(filepath) as fp:
        for i, line in enumerate(fp):
            action_found = False
            rate_found = False
            if i == ACTION_LINE:
                rtn_dic['Action'] = line.split(',')[1]
                action_found = True
            elif i == RATE_LINE:
                rtn_dic['SampleRate'] = int(line.split(',')[1])
                rate_found = True
            if (action_found and rate_found):
                break

    return rtn_dic


def parse_simple_file(filepath, ACTION_LINE = 2, RATE_LINE = 3):
    """
    Parse a data file formated in a simple format for 3rd-party files

    Args:
        string - filepath: filepath to SIM .txt file
        int - ACTION_LINE: A const value to represent which fileline
            has the action being performed
        int - RATE_LINE: A const value representing which fileline
            has the sample rate (in Hz) of the data collected.
    
    Return:
        dict with the following:
            'Time_s': timestamp array in seconds
            'AccX': Array of accelerations along the X-axis(this typically points forward) in m/s/s
            'AccY': Array of accelerations along the Y-axis(this typically point downward) in m/s/s
            'AccZ': Array of accelerations along the Z-axis(this typically points leftward) in m/s/s
            'AccM': Array of magnitude acceleration
            'Action': Activity being logged (eg 'walking', 'squating', etc)
            'SampleRate': Rate of data collection[in Hz]
    """
    df = pd.read_csv(filepath, skiprows=4)

    df['AccM'] = [np.sqrt(np.power(df['AccX'][i], 2) + np.power(df['AccY'][i], 2) + np.power(df['AccZ'][i], 2))
                    for i in range(len(df['AccX']))]
    rtn_dic = {'Time_s': df['Time'].values,
               'AccX': df['AccX'].values,
               'AccY': df['AccY'].values,
               'AccZ': df['AccZ'].values,
               'AccM': df['AccM'].values}

    with open(filepath) as fp:
        for i, line in enumerate(fp):
            action_found = False
            rate_found = False
            if i == ACTION_LINE:
                rtn_dic['Action'] = line.rstrip().split(',')[1]
                action_found = True
            elif i == RATE_LINE:
                rtn_dic['SampleRate'] = float(line.rstrip().split(',')[1])
                rate_found = True
            if (action_found and rate_found):
                break

    return rtn_dic


def create_simple_file(filepath, activity, sample_rate, df):
    """
    Create a file with a simple format. View README for more details

    Args:
        filepath (str) - where to place the new file
        activity (str) - activity the file represents
        sample_rate (float) - the rate the data was collected
        df (Dataframe) - dataframe containing file data
    """
    date = str(datetime.datetime.now())
    with open(filepath, mode='w') as file:
        csvwrite = csv.writer(file, 
                              delimiter=',', 
                              quotechar='"', 
                              quoting=csv.QUOTE_MINIMAL)
        #First row data
        csvwrite.writerow([f"//Date Created {date}"])
        # Second row units
        csvwrite.writerow([f"//Units: sec, m/s/s"])
        # Thrid row activity
        csvwrite.writerow(["Action", activity])
        # Fourth row sample rate
        csvwrite.writerow(["SampleRate", sample_rate])

    #Append data
    df.to_csv(filepath, mode='a', index=False)