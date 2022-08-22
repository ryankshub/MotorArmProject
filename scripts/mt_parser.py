#! /usr/bin/env python3

# Project import

# Python import

# 3rd-party import
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def plot_all_mt_data(filepath, title, psd_plot=True):
    """
    Plot acceleration from all 3 axis from MT IMU Software.

    Args:
        string filepath - filepath of MT data file
        string title - Title for plot
        bool psd_plot - Set true to plot acceleration alongside frequency domain, 
                        false to plot alongside free accel (w/o gravity)
    """
    data_dict = parse_mt(filepath)

    fig, axs = plt.subplots(3,2)
    fig.suptitle(title)
    fs = 1/np.mean(np.diff(data_dict['Time_s']))

    # Set up for Acc X
    axs[0][0].plot(data_dict['Time_s'], data_dict["AccX"], color="tab:red")
    #axs[0][0].set_xlabel("Time(ms)")
    axs[0][0].set_ylabel("Acc X")
    axs[0][0].set_ylim([-14,14])

    
    if (psd_plot):
        # Plot Freq domain
        nPts = len(data_dict["AccX"])
        f, Pxx = signal.welch(data_dict['AccX'], fs, nperseg=nPts)

        axs[0][1].plot(f, Pxx, color="tab:red")

        #axs[0][1].set_xlabel("Freq(hz)")
        axs[0][1].set_ylabel("Power")
        axs[0][1].set_xlim([0,10])
    else:
        # Set up for Free Acc X (no gravity)
        axs[0][1].plot(data_dict['Time_s'], data_dict["FreeAccX"], color="tab:red")
        #axs[0][1].set_xlabel("Time(ms)")
        axs[0][1].set_ylabel("Free Acc X")

    # Set up for AccY 
    axs[1][0].plot(data_dict['Time_s'], data_dict["AccY"], color="tab:blue")
    #axs[1][0].set_xlabel("Time(ms)")
    axs[1][0].set_ylabel("Acc Y")
    axs[1][0].set_ylim([-14,14])

    if (psd_plot):
        # Plot Freq domain
        nPts = len(data_dict["AccY"])
        f, Pxx = signal.welch(data_dict['AccY'], fs, nperseg=nPts)

        axs[1][1].plot(f, Pxx, color="tab:blue")
        #axs[1][1].set_xlabel("Freq(hz)")
        axs[1][1].set_ylabel("Power")
        axs[1][1].set_xlim([0,10])
    else:
        # Set up for Free Acc Y
        axs[1][1].plot(data_dict['Time_s'], data_dict["FreeAccY"], color="tab:blue")
        #axs[1][1].set_xlabel("Time(ms)")
        axs[1][1].set_ylabel("Free Acc Y")

    # Set up for AccZ
    axs[2][0].plot(data_dict['Time_s'], data_dict["AccZ"], color="tab:green")
    axs[2][0].set_xlabel("Time(ms)")
    axs[2][0].set_ylabel("Acc Z")
    axs[2][0].set_ylim([-14,14])

    # Set up for Free Acc Z
    if (psd_plot):
        # Plot Freq domain
        nPts = len(data_dict["AccZ"])
        f, Pxx = signal.welch(data_dict['AccZ'], fs, nperseg=nPts)

        axs[2][1].plot(f, Pxx, color="tab:green")
        axs[2][1].set_xlabel("Freq(hz)")
        axs[2][1].set_ylabel("Power")
        axs[2][1].set_xlim([0,10])
    else:
        axs[2][1].plot(data_dict['Time_s'], data_dict["FreeAccX"], color="tab:green")
        axs[2][1].set_xlabel("Time(ms)")
        axs[2][1].set_ylabel("Free Acc Z(m/s^2)")


    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.6)
    plt.show()


def plot_mt_data(filepath, title, key, psd_plot=True):
    """
    Plot subset of data from MT IMU Software

    Args:
        string filepath - filepath to MT data file
        string title - title of plot
        string or array key - If key is a string, parses mt data file and pulls
            data from corresponding key. If key is not a string, assumed to be 
            raw_data
        bool psd_plot - set true to plot psd alongside acceleration
    """ 
    data_dict = parse_mt(filepath)

    if (psd_plot):
        fig, axs = plt.subplots(1,2)
        fig.suptitle(title)
        fs = 1/np.mean(np.diff(data_dict['Time_s']))

        # Set up for Acc X
        accel_data = 0
        if (type(key) == str):
            accel_data = data_dict[key]
        else:
            accel_data = key

        axs[0].plot(data_dict['Time_s'], accel_data, color="tab:blue")
        axs[0].set_xlabel("Time(ms)")
        axs[0].set_ylabel("AccY")
        #axs[0][0].set_ylim([-14,14])

        # Plot Freq domain
        nPts = len(accel_data)
        f, Pxx = signal.welch(accel_data, fs, nperseg=nPts)

        axs[1].plot(f, Pxx, color="tab:red")
        axs[1].set_xlabel("Freq(hz)")
        axs[1].set_ylabel("Power")
        axs[1].set_xlim([0,10])
    
    else:
        fig, ax = plt.subplots(1,1)
        fig.suptitle(title)
        ax.plot(data_dict['Time_s'], accel_data, color="tab:blue")
        ax.set_xlabel("Time(ms)")
        ax.set_ylabel(key)

    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.6)
    plt.show()