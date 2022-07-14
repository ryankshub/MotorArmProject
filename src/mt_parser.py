#! /usr/bin/env python3

# Project import

# Python import

# 3rd-party import
import matplotlib.pyplot as plt
import pandas as pd

def parse_mt(filepath):
    """
    Parse a data file from MT IMU Software. 

    Args:
        string - filepath: filepath to MT .txt file
    
    Return:
        dict of 7 arrays with 'Time_ms', 'AccX', 'AccY', 'AccZ', 
            'FreeAccX', 'FreeAccY', and 'FreeAccZ'
    """
    df = pd.read_csv(filepath, skiprows=4, sep='\t')
    # Output data rate is 100Hz or 10ms between samples
    start_sample = df['PacketCounter'][0]
    df['Time_ms'] = [10 * (df['PacketCounter'][i] - start_sample) for i in range(len(df['PacketCounter']))]
    rtn_dic = {'Time_ms': df['Time_ms'].values,
               'AccX': df['Acc_X'].values,
               'AccY': df['Acc_Y'].values,
               'AccZ': df['Acc_Z'].values,
               'FreeAccX': df['FreeAcc_X'].values,
               'FreeAccY': df['FreeAcc_Y'].values,
               'FreeAccZ': df['FreeAcc_Z'].values}
    return rtn_dic


def plot_mt_data(filepath, title):
    """
    Plot data from MT IMU Software.
    """
    data_dict = parse_mt(filepath)

    fig, axs = plt.subplots(3,2)
    fig.suptitle(title)
    # Set up for Acc X
    axs[0][0].plot(data_dict['Time_ms'], data_dict["AccX"], color="tab:red")
    axs[0][0].set_xlabel("Time(ms)")
    axs[0][0].set_ylabel("Acc X(m/s^2)")

    # Set up for Free Acc X (no gravity)
    axs[0][1].plot(data_dict['Time_ms'], data_dict["FreeAccX"], color="tab:red")
    axs[0][1].set_xlabel("Time(ms)")
    axs[0][1].set_ylabel("Free Acc X(m/s^2)")

    # Set up for AccY 
    axs[1][0].plot(data_dict['Time_ms'], data_dict["AccY"], color="tab:blue")
    axs[1][0].set_xlabel("Time(ms)")
    axs[1][0].set_ylabel("Acc Y(m/s^2)")

    # Set up for Free Acc Y
    axs[1][1].plot(data_dict['Time_ms'], data_dict["FreeAccY"], color="tab:blue")
    axs[1][1].set_xlabel("Time(ms)")
    axs[1][1].set_ylabel("Free Acc Y(m/s^2)")

    # Set up for AccZ
    axs[2][0].plot(data_dict['Time_ms'], data_dict["AccZ"], color="tab:green")
    axs[2][0].set_xlabel("Time(ms)")
    axs[2][0].set_ylabel("Acc Z(m/s^2)")

    # Set up for Free Acc Z
    axs[2][1].plot(data_dict['Time_ms'], data_dict["FreeAccX"], color="tab:green")
    axs[2][1].set_xlabel("Time(ms)")
    axs[2][1].set_ylabel("Free Acc Z(m/s^2)")


    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.6)
    plt.show()
