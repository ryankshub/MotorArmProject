#! /usr/bin/env python3

# Plotting script for data analysis

# Python import
import argparse
import os
import sys
import re

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import 
from utils import apply_filter, apply_zero_phase_filter, parse_mt_file, \
    parse_simple_file, shred_data

# 3rd-party import
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal, stats


def plot_profile(filename, data, end_time, window_len, 
    lowpass, order, cutoff, sample_rate):
    """
    """
    # Make subplot
    fig, axs = plt.subplots(3,1)
    fig.suptitle(f"{filename} at {end_time}")

    # Plot raw data
    start_time = end_time - window_len
    time_axis = np.linspace(start_time, end_time, num=len(data))
    axs[0].plot(time_axis, data, label="Raw Data")
    axs[0].set_title("Acceleration data")
    axs[0].set_xlabel("Time (sec)")
    axs[0].set_ylabel("Accel Mag (m/s^2)")

    # Plot filter data
    if lowpass:
        filtered_data = apply_filter(data, sample_rate, 
            order, 'lowpass', cutoff)
    else:
        filtered_data = apply_zero_phase_filter(data, sample_rate, 
            order, 'lowpass', cutoff)
    peak_height_threshold = np.sort(filtered_data)[-2]
    peak_height_threshold = peak_height_threshold*.8
    axs[1].plot(time_axis, filtered_data, label="Filtered Data")
    peaks, _ = signal.find_peaks(filtered_data, height=peak_height_threshold)
    axs[1].plot(time_axis[peaks], filtered_data[peaks], "x")
    axs[1].set_title("Filtered Acceleration")
    axs[1].set_xlabel("Time (sec)")
    axs[1].set_ylabel("Accel Mag (m/s^2)")

    # Plot freq domain
    nPts = len(data)
    f, Pxx = signal.welch(data, sample_rate, nperseg=nPts)
    max_idx = np.argmax(Pxx)
    pSum = sum(Pxx)
    pNorm = Pxx/pSum
    ent = stats.entropy(pNorm)
    dom_freq = f[max_idx]
    dom_power = Pxx[max_idx]
    axs[2].plot(f, Pxx, color='orange')
    axs[2].set_title("Frequency Domain")
    axs[2].set_xlabel("Frequency")
    axs[2].set_ylabel("Power")
    axs[2].axvline(dom_freq, 
        label=f"Dom Freq {dom_freq:.03f} w/power: {dom_power:.03f} & ent: {ent:.03f}", 
        color='black')
    axs[2].legend()

    plt.subplots_adjust(left=0.1,
            bottom=0.1, 
            right=0.9, 
            top=0.9, 
            wspace=0.4, 
            hspace=0.6)

    plt.show()

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot windowed slices of \
        acceleration data for data analysis. Subplots are produced with \
        a top plot of raw acceleration magnitude, a filtered acceleration \
        with peak detection for steps detection, and a freq domain plot")
    parser.add_argument("plot_target", type=str, help="file or directory \
        containing acceleration profiles to plot")
    parser.add_argument("-d", "--dir",  action="store_true", help="Indicate \
        that plot_target is a directory contain files of acceleration profiles \
        instead of a single file")
    parser.add_argument("-l", "--list", action="store_true", help="Indicate \
        that plot_target is a list of filepaths")
    parser.add_argument("-z", "--categorize", action="store_true", help="Instead \
        of plotting subplots with raw, filtered, and frequency domain data; \
        create seperate plots for each. Useful for comparing different profiles")
    parser.add_argument("-f", "--filter", type=str, default="non_causal", 
        choices=["lowpass", "non_causal"], help="type of filter to apply to \
        data.")
    parser.add_argument("-o", "--order", type=int, default=4, help="Order of \
        filter")
    parser.add_argument("-c", "--cutoff", type=float, default=10.0, help="Cutoff \
        frequency of the filter")
    parser.add_argument("-w", "--window", type=float, default=3.0, help="Length \
        of the time window(in seconds). If window is -1.0, the whole file is used")
    parser.add_argument("-s", "--sample_rate", type=float, default=100.0, help="Sample \
        rate of the data collected")

    args = parser.parse_args()

    #Single file case:
    if not args.dir and not args.list:
        # Get filename
        filename = os.path.basename(args.plot_target)
        # Parse file
        if re.match(r"\AMT", filename):
            data_dict = parse_mt_file(args.plot_target)
        elif re.match(r"\ASIM", filename):
            data_dict = parse_simple_file(args.plot_target)
        else:
            raise Exception("Invalid File Format found")
        # Prep for plotting
        lowpass_bool = args.filter == "lowpass"
        if args.window < 0.0:
            window_time = data_dict['Time_s'][-1]
            plot_profile(filename, data_dict['AccM'], data_dict['Time_s'][-1],
                window_time, lowpass_bool, args.order, args.cutoff, 
                args.sample_rate)
        else:
            samples = shred_data(data_dict, interval=args.window)
            time_increment = 1.0/args.sample_rate
            end_time = args.window
            for sample in samples:
                plot_profile(filename, sample, end_time, args.window, 
                    lowpass_bool, args.order, args.cutoff, args.sample_rate)
                end_time = end_time + time_increment

        # plt.subplots_adjust(left=0.1,
        #     bottom=0.1, 
        #     right=0.9, 
        #     top=0.9, 
        #     wspace=0.4, 
        #     hspace=0.6)

        # plt.show()

