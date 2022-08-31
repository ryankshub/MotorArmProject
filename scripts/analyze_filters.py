#! /usr/bin/env python3

# File to plot and analysis filters

# Python imports
import argparse
import os
import sys
import time
# Project imports
# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from utils import apply_filter, apply_zero_phase_filter, parse_mt_file

# 3rd Party imports
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def plot_frequency_analysis(title, filepath, order, cutoff, fs, causal=True):
    # Parse data
    data_path = os.path.join(ROOT_PATH, filepath)
    data_dict = parse_mt_file(data_path)
    timestamps = data_dict["Time_s"]
    raw_data = data_dict["AccM"]

    # Get freq response
    b, a = signal.butter(order, cutoff, 'low', fs=fs)
    w, h = signal.freqz(b,a, fs=fs, worN=8000)

    # Get filt data
    filt_data = None
    if (causal):
        st = time.process_time()
        filt_data = apply_filter(raw_data, fs, order, 'low', cutoff)
        et = time.process_time()
        print(f"Compute Time LFilter: {et - st}")
    else:
        st = time.process_time()
        filt_data = apply_zero_phase_filter(raw_data, fs, order, 'low', cutoff)
        et = time.process_time()
        print(f"Compute Time FiltFilt: {et - st}")
    # Get peak times 
    peaks, _ = signal.find_peaks(filt_data)
    peak_times = timestamps[peaks]

    # Plotting time!!
    # Plot freq response
    fig_fr, ax_fr = plt.subplots()
    fig_fr.suptitle(title)
    ax_fr.plot(w, np.abs(h), 'b')
    ax_fr.plot(cutoff, 0.5*np.sqrt(2), 'ko')
    ax_fr.axvline(cutoff, color='k')
    ax_fr.set_xlim(0, 5)
    ax_fr.set_title("Lowpass Filter Frequency Response")
    ax_fr.set_xlabel('Frequency [Hz]')
    ax_fr.grid()

    # Plot raw data and filtered data
    fig_d, ax_d = plt.subplots()
    fig_d.suptitle(title)
    ax_d.plot(timestamps, raw_data, 'b-', label='data')
    ax_d.plot(timestamps, filt_data, 'g-', label="filtered data")
    ax_d.set_xlabel('Time [sec]')
    ax_d.set_ylabel('Accel [m/s/s]')
    ax_d.set_title(f"Effects of Lowpass Filter: Cutoff {cutoff}")
    ax_d.set_xlim(10, 20)
    ax_d.set_ylim(6,14)
    ax_d.grid()
    ax_d.legend()

    # Plot when steps took place
    fig_s, ax_s = plt.subplots(2, 1)
    fig_s.suptitle(title)
    ax_s[0].plot(timestamps, raw_data, 'b-')
    ax_s[1].plot(timestamps, filt_data, 'g-')
    for peak_time in peak_times:
        ax_s[0].axvline(peak_time, color='k')
        ax_s[1].axvline(peak_time, color='k')
    ax_s[0].grid()
    ax_s[1].grid()
    ax_s[0].set_title("Steps detected during signal")
    ax_s[0].set_xlim(10, 20)
    ax_s[1].set_xlim(10, 20)
    ax_s[0].set_ylim(6,14)
    ax_s[1].set_ylim(6,14)
    ax_s[1].set_xlabel('Time [sec]')
    ax_s[0].set_ylabel('Accel [m/s/s]')
    ax_s[1].set_ylabel('Accel [m/s/s]')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Produce 3 plots: the freq "
        "response of a butterworth filter, the effect of the filter on data, "
        "and steps aligned with filtered data")
    parser.add_argument('datafile', type=str, help="Filepath to data to analyze")
    parser.add_argument('--order', '-o', type=int, default=3, help="Butterworth filter order")
    parser.add_argument('--cutoff', '-c', type=float, default=1.4, help="Cutoff Frequency")
    parser.add_argument('--sample_freq', '-s', type=float, default=100.0, 
        help="Sampling freqency")
    parser.add_argument("--title", '-t', type=str, help="Figure title for each plot")
    parser.add_argument('--zero_phase', '-z', action="store_true", default=False)

    args = parser.parse_args()
    print(args)
    filepath = args.datafile
    order = args.order
    cutoff = args.cutoff
    fs = args.sample_freq
    title = args.title
    causal = not args.zero_phase

    plot_frequency_analysis(title, filepath, order=order, cutoff=cutoff, fs=fs, causal=causal)

    plt.show()