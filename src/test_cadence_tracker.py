#!/usr/bin/env python3

# Project Import
from cadence_tracker import CadenceTracker
import mt_parser

# Python import

# 3rd-party import
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Test file for CadenceTracker
# TODO: add this to unit test folder

# CT_50 = CadenceTracker(freq_Hz = 500, time_window_ms=50)
# CT_100 = CadenceTracker(freq_Hz = 500, time_window_ms=100)
# CT_200 = CadenceTracker(freq_Hz = 500, time_window_ms=200)

# CT_50.add_measurement(9.81)
# print(f"CT_50 data: {CT_50._data}")
# CT_200.add_datum([9.81, 0, 6])
# print(f"CT_200 data: {CT_200._data}")
# CT_200.clear_data()
# print(f"CT_200 data: {CT_200._data}")
# test = [1.1*i for i in range(30)]
# CT_50.add_datum(test)
# print(f"CT_50 data: {CT_50._data}")
# print(f"CT_50 cadence: {CT_50.calculate_cadence()}")
# print(f"CT_100 cadence: {CT_100.calculate_cadence()}")

filepath = '../data/cadence_test_data/MT_012006A8-2022-07-12-16h40_000_36-000.txt'
#mt_parser.plot_all_mt_data(filepath, "Raw Acceleration and PSD plots for 0.5ms stride")
data_dict = mt_parser.parse_mt(filepath)
time_steps = data_dict['Time_s']
raw_data = data_dict['AccY']
#mt_parser.plot_mt_data(filepath, "Raw Y-Acceleration and PSD plots for 0.5ms stride", "AccY")
#fs = 1/np.mean(np.diff(data_dict['Time_s']))
#filt_data = mt_parser.apply_filter(data_dict['AccY'], 3, 'lowpass', 0.9)
#mt_parser.plot_mt_data(filepath, "Filtered Y-Acceleration and PSD plots for 0.5ms stride", filt_data)
raw_data_sq = raw_data*-1#np.power(raw_data,2)

peaks, _ = signal.find_peaks(raw_data_sq)
plt.plot(raw_data_sq)
plt.plot(peaks, raw_data_sq[peaks], "x")
print(f"Number of steps {len(peaks)}")
plt.show()