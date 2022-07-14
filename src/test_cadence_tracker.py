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

filepath_05 = '../data/cadence_test_data/MT_012006A8-2022-07-12-16h40_000_36-000.txt'
steps_05 = 35
filepath_10 = '../data/cadence_test_data/MT_012006A8-2022-07-12-16h38_000_52-000.txt'
steps_10 = 51
filepath_12 = '../data/cadence_test_data/MT_012006A8-2022-07-12-16h42_000_57-000.txt'
steps_12 = 56

#mt_parser.plot_all_mt_data(filepath, "Raw Acceleration and PSD plots for 0.5ms stride")
data_dict05 = mt_parser.parse_mt(filepath_05)
data_dict10 = mt_parser.parse_mt(filepath_10)
data_dict12 = mt_parser.parse_mt(filepath_12)

# Calculate target cadence with 20 deg swing
target_05 = 10 / (data_dict05['Time_s'][-1]/steps_05)
target_10 = 10 / (data_dict10['Time_s'][-1]/steps_10)
target_12 = 10 / (data_dict12['Time_s'][-1]/steps_12)

print(f"Target Cadence for .5ms:{target_05}, 1.0ms:{target_10}, 1.2ms:{target_12}")

# Build low_pass filters
fs_05 = 1/np.mean(np.diff(data_dict05['Time_s']))
fs_10 = 1/np.mean(np.diff(data_dict10['Time_s']))
fs_12 = 1/np.mean(np.diff(data_dict12['Time_s']))

# Accel mag 
raw_steps_05 = len(signal.find_peaks(np.power(data_dict05['AccY'], 2))[0])
raw_steps_10 = len(signal.find_peaks(np.power(data_dict10['AccY'], 2))[0])
raw_steps_12 = len(signal.find_peaks(np.power(data_dict12['AccY'], 2))[0])

raw_stepsM_05 = len(signal.find_peaks(data_dict05['AccM'])[0])
raw_stepsM_10 = len(signal.find_peaks(data_dict10['AccM'])[0])
raw_stepsM_12 = len(signal.find_peaks(data_dict12['AccM'])[0])

print(f"Raw Accel-Y Steps:")
print(f"0.5: {raw_steps_05}, 1.0: {raw_steps_10}, 1.2: {raw_steps_12}")

print(f"Raw Accel-M Steps:")
print(f"0.5: {raw_stepsM_05}, 1.0: {raw_stepsM_10}, 1.2: {raw_stepsM_12}")

# Get filtered data
filt_data_05_1_4 = mt_parser.apply_filter(data_dict05['AccY'], fs_05, 3, 'lowpass', 1.4)
filt_data_05_2_0 = mt_parser.apply_filter(data_dict05['AccY'], fs_05, 3, 'lowpass', 2.0)
filt_data_05_2_5 = mt_parser.apply_filter(data_dict05['AccY'], fs_05, 3, 'lowpass', 2.5)
filt_data_05_3_0 = mt_parser.apply_filter(data_dict05['AccY'], fs_05, 3, 'lowpass', 3.0)

filt_dataM_05_1_4 = mt_parser.apply_filter(data_dict05['AccM'], fs_05, 3, 'lowpass', 1.4)
filt_dataM_05_2_0 = mt_parser.apply_filter(data_dict05['AccM'], fs_05, 3, 'lowpass', 2.0)
filt_dataM_05_2_5 = mt_parser.apply_filter(data_dict05['AccM'], fs_05, 3, 'lowpass', 2.5)
filt_dataM_05_3_0 = mt_parser.apply_filter(data_dict05['AccM'], fs_05, 3, 'lowpass', 3.0)

filt_data_10_1_4 = mt_parser.apply_filter(data_dict10['AccY'], fs_10, 3, 'lowpass', 1.4)
filt_data_10_2_0 = mt_parser.apply_filter(data_dict10['AccY'], fs_10, 3, 'lowpass', 2.0)
filt_data_10_2_5 = mt_parser.apply_filter(data_dict10['AccY'], fs_10, 3, 'lowpass', 2.5)
filt_data_10_3_0 = mt_parser.apply_filter(data_dict10['AccY'], fs_10, 3, 'lowpass', 3.0)

filt_dataM_10_1_4 = mt_parser.apply_filter(data_dict10['AccM'], fs_10, 3, 'lowpass', 1.4)
filt_dataM_10_2_0 = mt_parser.apply_filter(data_dict10['AccM'], fs_10, 3, 'lowpass', 2.0)
filt_dataM_10_2_5 = mt_parser.apply_filter(data_dict10['AccM'], fs_10, 3, 'lowpass', 2.5)
filt_dataM_10_3_0 = mt_parser.apply_filter(data_dict10['AccM'], fs_10, 3, 'lowpass', 3.0)

filt_data_12_1_4 = mt_parser.apply_filter(data_dict12['AccY'], fs_12, 3, 'lowpass', 1.4)
filt_data_12_2_0 = mt_parser.apply_filter(data_dict12['AccY'], fs_12, 3, 'lowpass', 2.0)
filt_data_12_2_5 = mt_parser.apply_filter(data_dict12['AccY'], fs_12, 3, 'lowpass', 2.5)
filt_data_12_3_0 = mt_parser.apply_filter(data_dict12['AccY'], fs_12, 3, 'lowpass', 3.0)

filt_dataM_12_1_4 = mt_parser.apply_filter(data_dict12['AccM'], fs_12, 3, 'lowpass', 1.4)
filt_dataM_12_2_0 = mt_parser.apply_filter(data_dict12['AccM'], fs_12, 3, 'lowpass', 2.0)
filt_dataM_12_2_5 = mt_parser.apply_filter(data_dict12['AccM'], fs_12, 3, 'lowpass', 2.5)
filt_dataM_12_3_0 = mt_parser.apply_filter(data_dict12['AccM'], fs_12, 3, 'lowpass', 3.0)

# Get steps
steps_05_1_4 = len(signal.find_peaks(np.power(filt_data_05_1_4, 2))[0])
steps_05_2_0 = len(signal.find_peaks(np.power(filt_data_05_2_0, 2))[0])
steps_05_2_5 = len(signal.find_peaks(np.power(filt_data_05_2_5, 2))[0])
steps_05_3_0 = len(signal.find_peaks(np.power(filt_data_05_3_0, 2))[0])

steps_10_1_4 = len(signal.find_peaks(np.power(filt_data_10_1_4, 2))[0])
steps_10_2_0 = len(signal.find_peaks(np.power(filt_data_10_2_0, 2))[0])
steps_10_2_5 = len(signal.find_peaks(np.power(filt_data_10_2_5, 2))[0])
steps_10_3_0 = len(signal.find_peaks(np.power(filt_data_10_3_0, 2))[0])

steps_12_1_4 = len(signal.find_peaks(np.power(filt_data_12_1_4, 2))[0])
steps_12_2_0 = len(signal.find_peaks(np.power(filt_data_12_2_0, 2))[0])
steps_12_2_5 = len(signal.find_peaks(np.power(filt_data_12_2_5, 2))[0])
steps_12_3_0 = len(signal.find_peaks(np.power(filt_data_12_3_0, 2))[0])

print(f"Accel-Y Steps with 0.5 ms cutoff freq:")
print(f"1.4: {steps_05_1_4}, 2.0: {steps_05_2_0}, 2.5: {steps_05_2_5}, 3.0: {steps_05_3_0}")

print(f"Accel-Y Steps with 1.0 ms cutoff freq:")
print(f"1.4: {steps_10_1_4}, 2.0: {steps_10_2_0}, 2.5: {steps_10_2_5}, 3.0: {steps_10_3_0}")

print(f"Accel-Y Steps with 1.2 ms cutoff freq:")
print(f"1.4: {steps_12_1_4}, 2.0: {steps_12_2_0}, 2.5: {steps_12_2_5}, 3.0: {steps_12_3_0}")


stepsM_05_1_4 = len(signal.find_peaks(filt_dataM_05_1_4)[0])
stepsM_05_2_0 = len(signal.find_peaks(filt_dataM_05_2_0)[0])
stepsM_05_2_5 = len(signal.find_peaks(filt_dataM_05_2_5)[0])
stepsM_05_3_0 = len(signal.find_peaks(filt_dataM_05_3_0)[0])

stepsM_10_1_4 = len(signal.find_peaks(filt_dataM_10_1_4)[0])
stepsM_10_2_0 = len(signal.find_peaks(filt_dataM_10_2_0)[0])
stepsM_10_2_5 = len(signal.find_peaks(filt_dataM_10_2_5)[0])
stepsM_10_3_0 = len(signal.find_peaks(filt_dataM_10_3_0)[0])

stepsM_12_1_4 = len(signal.find_peaks(filt_dataM_12_1_4)[0])
stepsM_12_2_0 = len(signal.find_peaks(filt_dataM_12_2_0)[0])
stepsM_12_2_5 = len(signal.find_peaks(filt_dataM_12_2_5)[0])
stepsM_12_3_0 = len(signal.find_peaks(filt_dataM_12_3_0)[0])

print(f"Accel-M Steps with 0.5 ms cutoff freq:")
print(f"1.4: {stepsM_05_1_4}, 2.0: {stepsM_05_2_0}, 2.5: {stepsM_05_2_5}, 3.0: {stepsM_05_3_0}")

print(f"Accel-M Steps with 1.0 ms cutoff freq:")
print(f"1.4: {stepsM_10_1_4}, 2.0: {stepsM_10_2_0}, 2.5: {stepsM_10_2_5}, 3.0: {stepsM_10_3_0}")

print(f"Accel-M Steps with 1.2 ms cutoff freq:")
print(f"1.4: {stepsM_12_1_4}, 2.0: {stepsM_12_2_0}, 2.5: {stepsM_12_2_5}, 3.0: {stepsM_12_3_0}")

#mt_parser.plot_mt_data(filepath, "Raw Y-Acceleration and PSD plots for 0.5ms stride", "AccY")
mt_parser.plot_mt_data(filepath_05, "Filtered Y-Acceleration and PSD plots for 0.5ms stride: 1.4Hz cutoff", filt_data_05_1_4)
mt_parser.plot_mt_data(filepath_05, "Filtered Y-Acceleration and PSD plots for 0.5ms stride: 2.0Hz cutoff", filt_data_05_2_0)
mt_parser.plot_mt_data(filepath_05, "Filtered Y-Acceleration and PSD plots for 0.5ms stride: 2.5Hz cutoff", filt_data_05_2_5)
mt_parser.plot_mt_data(filepath_05, "Filtered Y-Acceleration and PSD plots for 0.5ms stride: 3.0Hz cutoff", filt_data_05_3_0)

mt_parser.plot_mt_data(filepath_05, "Filtered Acceleration and PSD plots for 0.5ms stride: 1.4Hz cutoff", filt_dataM_05_1_4)
mt_parser.plot_mt_data(filepath_05, "Filtered Acceleration and PSD plots for 0.5ms stride: 2.0Hz cutoff", filt_dataM_05_2_0)
mt_parser.plot_mt_data(filepath_05, "Filtered Acceleration and PSD plots for 0.5ms stride: 2.5Hz cutoff", filt_dataM_05_2_5)
mt_parser.plot_mt_data(filepath_05, "Filtered Acceleration and PSD plots for 0.5ms stride: 3.0Hz cutoff", filt_dataM_05_3_0)

# peaks, _ = signal.find_peaks(raw_data_sq)
# plt.plot(raw_data_sq)
# plt.plot(peaks, raw_data_sq[peaks], "x")
# print(f"Number of steps {len(peaks)}")
# plt.show()