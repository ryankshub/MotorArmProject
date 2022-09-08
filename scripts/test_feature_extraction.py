#!/usr/bin/env python3

# Python import
import os
import sys
import time

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
from scipy import signal, stats

def get_entropy(Pxx):
    P_sum = sum(Pxx)
    Pxx_norm = Pxx/P_sum
    #return (-sum([P*np.log(P) for P in Pxx_norm]))
    return stats.entropy(Pxx_norm)


filepath_10 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_10_52.txt')
data_dict = parse_mt_file(filepath_10)
time_data = data_dict["Time_s"]
fs = 1/np.mean(np.diff(data_dict['Time_s']))
accel_data = data_dict["AccM"]

nPts = len(accel_data)
f, Pxx = signal.welch(accel_data, fs, nperseg=nPts)

print(f"Frequency {f}, Length: {len(f)}")
print(f"Power {Pxx}, Length: {len(Pxx)}")

# Feature Extraction time
start_time = time.time()
max_freq = f[np.argmax(Pxx)]
max_power = Pxx[np.argmax(Pxx)]
entropy = get_entropy(Pxx)
end_time = time.time()
clock_time = end_time - start_time
print(f"max_freq: {max_freq}")
print(f"max_power: {max_power}")
print(f"entropy {entropy}")
print(f"clock time: {clock_time}")