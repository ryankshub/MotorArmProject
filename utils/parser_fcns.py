#! /usr/bin/env python3
"""
Collection of parsers for the various data files in project
"""

# Project import

# Python import

# 3rd-party import
import numpy as np
import pandas as pd

def parse_mt_file(filepath, ACTION_LINE = 4):
    """
    Parse a data file from MT IMU Software. 

    Args:
        string - filepath: filepath to MT .txt file
        int - ACTION_LINE: A const value to represent which fileline
            has the action being performed
    
    Return:
        dict of 7 arrays with 'Time_s', 'AccX', 'AccY', 'AccZ', 
            'FreeAccX', 'FreeAccY', and 'FreeAccZ'
    """
    df = pd.read_csv(filepath, skiprows=5)
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
            if i == ACTION_LINE:
                rtn_dic['Action'] = line.split(',')[1]
                break

    return rtn_dic