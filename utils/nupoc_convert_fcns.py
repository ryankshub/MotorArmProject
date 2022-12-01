#!/usr/bin/env python3
"""
This file contains functions to convert datafile record from
Northwestern University Prosthetics-Orthotics Center
"""
# Project import


# Python import
import datetime
import os
import re

# 3rd-party import
import numpy as np
import pandas as pd
import scipy.io


def make_simple_filename(activity, wp_key):
    """
    Create a name for new simple file. The template is:
    SIM_[activity acronym]_[waypoint]_[data_generated].txt

    Args:
        activity (str) - activity the logged represents
        wp_key (str) - waypoint of interest for simple file

    Rtns:
        new filename for simple file
    """
    # Build base_str
    base_str = "SIM_"
    
    # Build Activity str
    boring_words = ["a", "an", "and", "the"]
    act_str = ""
    for word in activity.split(' '):
        if word not in boring_words:
            act_str += word[0].upper()
        if len(act_str) >= 3:
            break
    
    # Build Way Point str
    wp_str = ""
    wp_key = wp_key.replace('.','_')
    for word in wp_key.split('_'):
        wp_str += word.capitalize()
    
    # Build Date str
    date_str = str(datetime.datetime.now()).replace(' ', ':')

    # Build return str
    rtn_str = base_str + act_str + '_' + wp_str + '_' + date_str + '.txt'

    return rtn_str


def parse_action_dict(filepath):
    """
    Given a key file with task number and task descriptions, return
    a dictionary contain mapping

    Args:
        filepath - filepath to key file

    Rtn:
        action_dict - a dictionary with task numbers(int) as keys and task
            descriptions as values
    """
    # Get filename and extension
    filename = os.path.basename(filepath)
    fileext = os.path.splitext(filename)[1]

    # Parse file into pandas dataframe
    if fileext == '.xlsx':
        df = pd.read_excel(filepath)
    else:
        df = pd.read_csv(filepath)

    subdf = df.loc[:,['Task number', 'Task Description']]
    lim = subdf['Task number'].notna().idxmin()
    subdf = subdf[:lim]
    return dict(zip(subdf['Task number'], subdf['Task Description']))


def parse_mat_file(filepath, wp_key, activity="walking"):
    """
    Parses a matfile from NUPOC measuring x,y,z positions of
    several waypoints. Returns the corresponding activity the
    file logges and a dataframe with the acceleration values of
    the waypoint. 

    Args:
        filepath - filepath to logged file
        wp_key (str) - name of interested waypoint
        activity (str) - activity described by matfile

    Rtn:
        activity (str) - brief description of activity
        subdf - data frame containing Frame, Time (sec), and 
            waypoint accelerations 
    """
    # Get data file
    mat_dic = scipy.io.loadmat(filepath)
    df = pd.DataFrame()

    # get frame col and time array
    df['Frame#'] = mat_dic['frame'][0] + 1
    time_arr = mat_dic['time'][0]

    # build x,y,z
    act_str = wp_key.ljust(15, ' ') #15 = length of all str key in the mat files
    idx = np.where(mat_dic['coordnames'] == act_str)[0][0]

    # Convert mm to m
    posx_arr = mat_dic['coordx'][:, idx]*.001
    posy_arr = mat_dic['coordy'][:, idx]*.001
    posz_arr = mat_dic['coordz'][:, idx]*.001

    # get time diff
    time_diff = time_arr[1:] - time_arr[:-1]
    
    # Get position difference
    posx_diff = posx_arr[1:] - posx_arr[:-1]
    posy_diff = posy_arr[1:] - posy_arr[:-1]
    posz_diff = posz_arr[1:] - posz_arr[:-1]

    # get velocities
    vecx_arr = posx_diff / time_diff
    vecx_arr = np.insert(vecx_arr, 0, 0.0)
    vecy_arr = posy_diff / time_diff
    vecy_arr = np.insert(vecy_arr, 0, 0.0)
    vecz_arr = posz_diff / time_diff
    vecz_arr = np.insert(vecz_arr, 0, 0.0)

    # get velocity differences
    vecx_diff = vecx_arr[1:] - vecx_arr[:-1]
    vecy_diff = vecy_arr[1:] - vecy_arr[:-1]
    vecz_diff = vecz_arr[1:] - vecz_arr[:-1] 

    # get accelerations
    accx_arr = vecx_diff / time_diff
    accx_arr = np.insert(accx_arr, 0, 0.0)
    accy_arr = vecy_diff / time_diff
    accy_arr = np.insert(accy_arr, 0, 0.0)
    accz_arr = vecz_diff / time_diff
    accz_arr = np.insert(accz_arr, 0, 0.0)

    # Add time, accx, accy, and accz columns
    df['Time'], df['AccX'], df['AccY'], df['AccZ'] = [time_arr, accx_arr, accy_arr, accz_arr]

    return activity, df


def parse_trimmed_file(filepath, wp_key, action_dict):
    """
    Parses a logfile from NUPOC measuring x,y,z positions of
    several waypoints. Returns the corresponding activity the
    file logges and a dataframe with the acceleration values of
    the waypoint. 

    Args:
        filepath - filepath to logged file
        wp_key (str) - name of interested waypoint
        action_dict - map of activity id to descriptions

    Rtn:
        activity (str) - brief description of activity
        subdf - data frame containing Frame, Time (sec), and 
            waypoint accelerations 
    """
    # Get data frame
    df = pd.read_csv(filepath, skiprows=3, sep='\t')

    # Get Activity
    filename = os.path.basename(filepath)
    activity_num = int(re.split(r'[a-zA-Z|_|.]+', filename)[1])
    activity = action_dict[activity_num].lower()

    # Get subset of data
    tgt = df.columns.get_loc(wp_key)
    subdf = df.iloc[:,[0, 1, tgt, tgt+1, tgt+2]][2:]
    pos = ['PosX', 'PosY', 'PosZ']
    mapper = {subdf.columns[i]:pos[i-2] for i in range(2, len(pos)+2)}
    subdf.rename(columns=mapper, inplace=True)
    subdf.reset_index(drop=True, inplace=True)
    
    # Convert from mm to m 
    posx_arr = subdf.PosX.to_numpy(dtype=float)*.001
    posy_arr = subdf.PosY.to_numpy(dtype=float)*.001
    posz_arr = subdf.PosZ.to_numpy(dtype=float)*.001

    # get time arr
    time_arr = subdf.Time.to_numpy(dtype=float)
    time_diff = time_arr[1:] - time_arr[:-1]
    
    # Get position difference
    posx_diff = posx_arr[1:] - posx_arr[:-1]
    posy_diff = posy_arr[1:] - posy_arr[:-1]
    posz_diff = posz_arr[1:] - posz_arr[:-1]

    # get velocities
    vecx_arr = posx_diff / time_diff
    vecx_arr = np.insert(vecx_arr, 0, 0.0)
    vecy_arr = posy_diff / time_diff
    vecy_arr = np.insert(vecy_arr, 0, 0.0)
    vecz_arr = posz_diff / time_diff
    vecz_arr = np.insert(vecz_arr, 0, 0.0)

    # get velocity differences
    vecx_diff = vecx_arr[1:] - vecx_arr[:-1]
    vecy_diff = vecy_arr[1:] - vecy_arr[:-1]
    vecz_diff = vecz_arr[1:] - vecz_arr[:-1] 

    # get accelerations
    accx_arr = vecx_diff / time_diff
    accx_arr = np.insert(accx_arr, 0, 0.0)
    accy_arr = vecy_diff / time_diff
    accy_arr = np.insert(accy_arr, 0, 0.0)
    accz_arr = vecz_diff / time_diff
    accz_arr = np.insert(accz_arr, 0, 0.0)

    # Drop Position
    subdf.drop(columns=['PosX', 'PosY', 'PosZ'], inplace=True)
    subdf['AccX'], subdf['AccY'], subdf['AccZ'] = [accx_arr, accy_arr, accz_arr]

    return activity, subdf