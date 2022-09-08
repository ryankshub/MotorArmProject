#!/usr/bin/env python3

# Python import
import os
import sys

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from src import CadenceTracker
from utils import parse_mt_file, apply_filter

# 3rd-party import
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


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
    data_dict = parse_mt_file(filepath)

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
        axs[0].set_ylabel("Acceleration[m/s/s]")
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
    #plt.show()
    max_idx = np.argmax(Pxx)
    max_freq = f[max_idx]
    max_pow = Pxx[max_idx]
    return max_freq, max_pow


if __name__ == "__main__":
    # Anaylsis file to test step count
    filepath_05 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_05_36.txt')
    filepath_08 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_08_49.txt')
    filepath_10 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_10_52.txt')
    filepath_12 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_12_57.txt')
    filepath_14 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_14_60.txt')

    cutpath = os.path.join(ROOT_PATH, "data/non_walking_data/MT_RKS_Cut.txt")
    pourpath = os.path.join(ROOT_PATH, "data/non_walking_data/MT_RKS_Pour.txt")
    reachpath = os.path.join(ROOT_PATH, "data/non_walking_data/MT_RKS_Reach.txt")
    spinpath = os.path.join(ROOT_PATH, "data/non_walking_data/MT_RKS_Spin.txt")
    squatpath = os.path.join(ROOT_PATH, "data/non_walking_data/MT_RKS_Squat.txt")

    #mt_parser.plot_all_mt_data(filepath, "Raw Acceleration and PSD plots for 0.5ms stride")
    max_freq_05, max_pow_05 = plot_mt_data(filepath_05, "Time and Freq Domain of Walking 0.5ms data", key="AccM")
    max_freq_08, max_pow_08 = plot_mt_data(filepath_08, "Time and Freq Domain of Walking 0.8ms data", key="AccM")
    max_freq_10, max_pow_10 = plot_mt_data(filepath_10, "Time and Freq Domain of Walking 1.0ms data", key="AccM")
    max_freq_12, max_pow_12 = plot_mt_data(filepath_12, "Time and Freq Domain of Walking 1.2ms data", key="AccM")
    max_freq_14, max_pow_14 = plot_mt_data(filepath_14, "Time and Freq Domain of Walking 1.4ms data", key="AccM")
    max_freq_cut, max_pow_cut = plot_mt_data(cutpath, "Time and Freq Domain of Cutting data", key="AccM")
    max_freq_pour, max_pow_pour = plot_mt_data(pourpath, "Time and Freq Domain of Pouring data", key="AccM")
    max_freq_reach, max_pow_reach = plot_mt_data(reachpath, "Time and Freq Domain of Reaching data", key="AccM")
    max_freq_spin, max_pow_spin = plot_mt_data(spinpath, "Time and Freq Domain of Spinning data", key="AccM")
    max_freq_squat, max_pow_squat = plot_mt_data(squatpath, "Time and Freq Domain of Squating data", key="AccM")

    x_names = ["Walking_05", "Walking_08", "Walking_10", "Walking_12", "Walking_14", 
        "Cutting", "Pouring", "Reaching", "Spinning", "Squating"]
    y_freq = [max_freq_05, max_freq_08, max_freq_10, max_freq_12, max_freq_14, 
        max_freq_cut, max_freq_pour, max_freq_reach, max_freq_spin, max_freq_squat]
    y_power = [max_pow_05, max_pow_08, max_pow_10, max_pow_12, max_pow_14,
        max_pow_cut, max_pow_pour, max_pow_reach, max_pow_spin, max_pow_squat]
    color_names =["blue", "blue", "blue", "blue", "blue", "red", "red", "red", "red", "red"]

    fig, ax = plt.subplots(2,1,sharex=True)
    fig.suptitle("Simple FFT Classifier analysis")
    ax[0].bar(x=x_names, height=y_freq, width=0.5, color=color_names)
    ax[0].set_title("Dominant Frequency based on activity")
    #ax[0].set_xlabel("Activities")
    ax[0].set_ylabel("Freq [Hz]")

    ax[1].bar(x=x_names, height=y_power, width=0.5, color=color_names)
    ax[1].set_title("Intensities at Dominant Frequencies")
    ax[1].set_xlabel("Activities")
    ax[1].set_ylabel("Power")

    fig2, sax = plt.subplots()
    sax.scatter(y_freq, y_power, color=color_names)
    sax.set_title("Dominant Frequency Vs Power for classification")
    sax.set_xlabel("Dominant Frequency")
    sax.set_ylabel("Power")
    red_patch = mpatches.Patch(color='red', label='Non-walking Data')
    blue_patch = mpatches.Patch(color='blue', label='Walking Data')
    sax.legend(handles=[blue_patch, red_patch])

    plt.show()