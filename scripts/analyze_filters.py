#! /usr/bin/env python3

# File to plot and analysis filters

# Python imports
import argparse
import os
import sys

# Project imports
# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from utils import apply_filter, parse_mt_file

# 3rd Party imports
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def plot_lowpass_freq_resp(order, cutoff, fs):
    b, a = signal.butter(order, cutoff, 'low', fs=fs)
    w, h = signal.freqz(b,a, fs=fs, worN=8000)
    plt.plot(w, np.abs(h), 'b')
    plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
    plt.axvline(cutoff, color='k')
    plt.xlim(0, 5)
    plt.title("Lowpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid()


def plot_filter_applied(timestamps, data, order, cutoff, fs):
    filt_data = apply_filter(data, fs, order, 'low', cutoff)
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, data, 'b-', label='data')
    plt.plot(timestamps, filt_data, 'g-', label="filtered data")
    plt.xlabel('Time [sec]')
    plt.ylabel('Accel [m/s/s]')
    plt.grid()
    plt.legend()


def parse_relevent_data(filepath, abs=False):
    data_path = os.path.join(ROOT_PATH, filepath)
    data_dict = parse_mt_file(data_path)
    return data_dict["Time_s"], data_dict["AccM"]

if __name__ == "__main__":
    order = 3
    cutoff = 1.4
    fs = 100.0

    plot_lowpass_freq_resp(order=order, cutoff=cutoff, fs=fs)

    plt.show()