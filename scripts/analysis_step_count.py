#!/usr/bin/env python3

# Add Project root for imports
import os
import sys
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from src import CadenceTracker
from utils import parse_mt_file, apply_filter

# Python import

# 3rd-party import
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Anaylsis file to test step count
filepath_05 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_05_36.txt')
steps_05 = 35
filepath_08 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_08_49.txt')
steps_08 = 50
filepath_10 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_10_52.txt')
steps_10 = 52
filepath_12 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_12_57.txt')
steps_12 = 57
filepath_14 = os.path.join(ROOT_PATH, 'data/cadence_test_data/MT_RKS_14_60.txt')


#mt_parser.plot_all_mt_data(filepath, "Raw Acceleration and PSD plots for 0.5ms stride")
data_dict05 = parse_mt_file(filepath_05)
data_dict08 = parse_mt_file(filepath_08)
data_dict10 = parse_mt_file(filepath_10)
data_dict12 = parse_mt_file(filepath_12)
data_dict14 = parse_mt_file(filepath_14)


# Determine frequency of data:
fs_05 = 1/np.mean(np.diff(data_dict05['Time_s']))
print(f"Frequency of 0.5ms data: {fs_05}")
fs_08 = 1/np.mean(np.diff(data_dict08['Time_s']))
print(f"Frequency of 0.8ms data: {fs_08}")
fs_10 = 1/np.mean(np.diff(data_dict10['Time_s']))
print(f"Frequency of 1.0ms data: {fs_10}")
fs_12 = 1/np.mean(np.diff(data_dict12['Time_s']))
print(f"Frequency of 1.2ms data: {fs_12}")
fs_14 = 1/np.mean(np.diff(data_dict14["Time_s"]))
print(f"Frequency of 1.4ms data: {fs_14}")
print()


# Count Raw Steps from Y-Accel and Accel-M
raw_steps_05 = len(signal.find_peaks(np.power(data_dict05['AccY'], 2))[0])
raw_steps_08 = len(signal.find_peaks(np.power(data_dict08['AccY'], 2))[0])
raw_steps_10 = len(signal.find_peaks(np.power(data_dict10['AccY'], 2))[0])
raw_steps_12 = len(signal.find_peaks(np.power(data_dict12['AccY'], 2))[0])
raw_steps_14 = len(signal.find_peaks(np.power(data_dict14['AccY'], 2))[0])

raw_stepsM_05 = len(signal.find_peaks(data_dict05['AccM'])[0])
raw_stepsM_08 = len(signal.find_peaks(data_dict08['AccM'])[0])
raw_stepsM_10 = len(signal.find_peaks(data_dict10['AccM'])[0])
raw_stepsM_12 = len(signal.find_peaks(data_dict12['AccM'])[0])
raw_stepsM_14 = len(signal.find_peaks(data_dict14['AccM'])[0])

print(f"Raw Accel-Y Steps:")
print(f"0.5: {raw_steps_05}\n",
      f"0.8: {raw_steps_08}\n",
      f"1.0: {raw_steps_10}\n", 
      f"1.2: {raw_steps_12}\n",
      f"1.4: {raw_steps_14}\n")

print(f"Raw Accel-M Steps:")
print(f"0.5: {raw_stepsM_05}\n",
      f"0.8: {raw_stepsM_08}\n",
      f"1.0: {raw_stepsM_10}\n",
      f"1.2: {raw_stepsM_12}\n",
      f"1.4: {raw_stepsM_14}\n")


# Get filtered data
filt_data_05_1_4 = apply_filter(data_dict05['AccY'], fs_05, 3, 'lowpass', 1.4)
filt_data_05_2_0 = apply_filter(data_dict05['AccY'], fs_05, 3, 'lowpass', 2.0)
filt_data_05_2_5 = apply_filter(data_dict05['AccY'], fs_05, 3, 'lowpass', 2.5)
filt_data_05_3_0 = apply_filter(data_dict05['AccY'], fs_05, 3, 'lowpass', 3.0)

filt_dataM_05_1_4 = apply_filter(data_dict05['AccM'], fs_05, 3, 'lowpass', 1.4)
filt_dataM_05_2_0 = apply_filter(data_dict05['AccM'], fs_05, 3, 'lowpass', 2.0)
filt_dataM_05_2_5 = apply_filter(data_dict05['AccM'], fs_05, 3, 'lowpass', 2.5)
filt_dataM_05_3_0 = apply_filter(data_dict05['AccM'], fs_05, 3, 'lowpass', 3.0)

filt_data_08_1_4 = apply_filter(data_dict08['AccY'], fs_08, 3, 'lowpass', 1.4)
filt_data_08_2_0 = apply_filter(data_dict08['AccY'], fs_08, 3, 'lowpass', 2.0)
filt_data_08_2_5 = apply_filter(data_dict08['AccY'], fs_08, 3, 'lowpass', 2.5)
filt_data_08_3_0 = apply_filter(data_dict08['AccY'], fs_08, 3, 'lowpass', 3.0)

filt_dataM_08_1_4 = apply_filter(data_dict08['AccM'], fs_08, 3, 'lowpass', 1.4)
filt_dataM_08_2_0 = apply_filter(data_dict08['AccM'], fs_08, 3, 'lowpass', 2.0)
filt_dataM_08_2_5 = apply_filter(data_dict08['AccM'], fs_08, 3, 'lowpass', 2.5)
filt_dataM_08_3_0 = apply_filter(data_dict08['AccM'], fs_08, 3, 'lowpass', 3.0)

filt_data_10_1_4 = apply_filter(data_dict10['AccY'], fs_10, 3, 'lowpass', 1.4)
filt_data_10_2_0 = apply_filter(data_dict10['AccY'], fs_10, 3, 'lowpass', 2.0)
filt_data_10_2_5 = apply_filter(data_dict10['AccY'], fs_10, 3, 'lowpass', 2.5)
filt_data_10_3_0 = apply_filter(data_dict10['AccY'], fs_10, 3, 'lowpass', 3.0)

filt_dataM_10_1_4 = apply_filter(data_dict10['AccM'], fs_10, 3, 'lowpass', 1.4)
filt_dataM_10_2_0 = apply_filter(data_dict10['AccM'], fs_10, 3, 'lowpass', 2.0)
filt_dataM_10_2_5 = apply_filter(data_dict10['AccM'], fs_10, 3, 'lowpass', 2.5)
filt_dataM_10_3_0 = apply_filter(data_dict10['AccM'], fs_10, 3, 'lowpass', 3.0)

filt_data_12_1_4 = apply_filter(data_dict12['AccY'], fs_12, 3, 'lowpass', 1.4)
filt_data_12_2_0 = apply_filter(data_dict12['AccY'], fs_12, 3, 'lowpass', 2.0)
filt_data_12_2_5 = apply_filter(data_dict12['AccY'], fs_12, 3, 'lowpass', 2.5)
filt_data_12_3_0 = apply_filter(data_dict12['AccY'], fs_12, 3, 'lowpass', 3.0)

filt_dataM_12_1_4 = apply_filter(data_dict12['AccM'], fs_12, 3, 'lowpass', 1.4)
filt_dataM_12_2_0 = apply_filter(data_dict12['AccM'], fs_12, 3, 'lowpass', 2.0)
filt_dataM_12_2_5 = apply_filter(data_dict12['AccM'], fs_12, 3, 'lowpass', 2.5)
filt_dataM_12_3_0 = apply_filter(data_dict12['AccM'], fs_12, 3, 'lowpass', 3.0)

filt_data_14_1_4 = apply_filter(data_dict14['AccY'], fs_14, 3, 'lowpass', 1.4)
filt_data_14_2_0 = apply_filter(data_dict14['AccY'], fs_14, 3, 'lowpass', 2.0)
filt_data_14_2_5 = apply_filter(data_dict14['AccY'], fs_14, 3, 'lowpass', 2.5)
filt_data_14_3_0 = apply_filter(data_dict14['AccY'], fs_14, 3, 'lowpass', 3.0)

filt_dataM_14_1_4 = apply_filter(data_dict14['AccM'], fs_14, 3, 'lowpass', 1.4)
filt_dataM_14_2_0 = apply_filter(data_dict14['AccM'], fs_14, 3, 'lowpass', 2.0)
filt_dataM_14_2_5 = apply_filter(data_dict14['AccM'], fs_14, 3, 'lowpass', 2.5)
filt_dataM_14_3_0 = apply_filter(data_dict14['AccM'], fs_14, 3, 'lowpass', 3.0)


# Get steps
steps_05_1_4 = len(signal.find_peaks(np.power(filt_data_05_1_4, 2))[0])
steps_05_2_0 = len(signal.find_peaks(np.power(filt_data_05_2_0, 2))[0])
steps_05_2_5 = len(signal.find_peaks(np.power(filt_data_05_2_5, 2))[0])
steps_05_3_0 = len(signal.find_peaks(np.power(filt_data_05_3_0, 2))[0])

steps_08_1_4 = len(signal.find_peaks(np.power(filt_data_08_1_4, 2))[0])
steps_08_2_0 = len(signal.find_peaks(np.power(filt_data_08_2_0, 2))[0])
steps_08_2_5 = len(signal.find_peaks(np.power(filt_data_08_2_5, 2))[0])
steps_08_3_0 = len(signal.find_peaks(np.power(filt_data_08_3_0, 2))[0])

steps_10_1_4 = len(signal.find_peaks(np.power(filt_data_10_1_4, 2))[0])
steps_10_2_0 = len(signal.find_peaks(np.power(filt_data_10_2_0, 2))[0])
steps_10_2_5 = len(signal.find_peaks(np.power(filt_data_10_2_5, 2))[0])
steps_10_3_0 = len(signal.find_peaks(np.power(filt_data_10_3_0, 2))[0])

steps_12_1_4 = len(signal.find_peaks(np.power(filt_data_12_1_4, 2))[0])
steps_12_2_0 = len(signal.find_peaks(np.power(filt_data_12_2_0, 2))[0])
steps_12_2_5 = len(signal.find_peaks(np.power(filt_data_12_2_5, 2))[0])
steps_12_3_0 = len(signal.find_peaks(np.power(filt_data_12_3_0, 2))[0])

steps_14_1_4 = len(signal.find_peaks(np.power(filt_data_14_1_4, 2))[0])
steps_14_2_0 = len(signal.find_peaks(np.power(filt_data_14_2_0, 2))[0])
steps_14_2_5 = len(signal.find_peaks(np.power(filt_data_14_2_5, 2))[0])
steps_14_3_0 = len(signal.find_peaks(np.power(filt_data_14_3_0, 2))[0])

print(f"Accel-Y Steps with 0.5 ms cutoff freq:")
print(f"1.4: {steps_05_1_4} |",
      f"2.0: {steps_05_2_0} |", 
      f"2.5: {steps_05_2_5} |",
      f"3.0: {steps_05_3_0}")
print()

print(f"Accel-Y Steps with 0.8 ms cutoff freq:")
print(f"1.4: {steps_08_1_4} |",
      f"2.0: {steps_08_2_0} |", 
      f"2.5: {steps_08_2_5} |",
      f"3.0: {steps_08_3_0}")
print()

print(f"Accel-Y Steps with 1.0 ms cutoff freq:")
print(f"1.4: {steps_10_1_4} |",
      f"2.0: {steps_10_2_0} |", 
      f"2.5: {steps_10_2_5} |", 
      f"3.0: {steps_10_3_0}")
print()

print(f"Accel-Y Steps with 1.2 ms cutoff freq:")
print(f"1.4: {steps_12_1_4} |",
      f"2.0: {steps_12_2_0} |",
      f"2.5: {steps_12_2_5} |",
      f"3.0: {steps_12_3_0}")
print()

print(f"Accel-Y Steps with 1.4 ms cutoff freq:")
print(f"1.4: {steps_14_1_4} |",
      f"2.0: {steps_14_2_0} |",
      f"2.5: {steps_14_2_5} |",
      f"3.0: {steps_14_3_0}")
print()      

stepsM_05_1_4 = len(signal.find_peaks(filt_dataM_05_1_4)[0])
stepsM_05_2_0 = len(signal.find_peaks(filt_dataM_05_2_0)[0])
stepsM_05_2_5 = len(signal.find_peaks(filt_dataM_05_2_5)[0])
stepsM_05_3_0 = len(signal.find_peaks(filt_dataM_05_3_0)[0])

stepsM_08_1_4 = len(signal.find_peaks(filt_dataM_08_1_4)[0])
stepsM_08_2_0 = len(signal.find_peaks(filt_dataM_08_2_0)[0])
stepsM_08_2_5 = len(signal.find_peaks(filt_dataM_08_2_5)[0])
stepsM_08_3_0 = len(signal.find_peaks(filt_dataM_08_3_0)[0])

stepsM_10_1_4 = len(signal.find_peaks(filt_dataM_10_1_4)[0])
stepsM_10_2_0 = len(signal.find_peaks(filt_dataM_10_2_0)[0])
stepsM_10_2_5 = len(signal.find_peaks(filt_dataM_10_2_5)[0])
stepsM_10_3_0 = len(signal.find_peaks(filt_dataM_10_3_0)[0])

stepsM_12_1_4 = len(signal.find_peaks(filt_dataM_12_1_4)[0])
stepsM_12_2_0 = len(signal.find_peaks(filt_dataM_12_2_0)[0])
stepsM_12_2_5 = len(signal.find_peaks(filt_dataM_12_2_5)[0])
stepsM_12_3_0 = len(signal.find_peaks(filt_dataM_12_3_0)[0])

stepsM_14_1_4 = len(signal.find_peaks(filt_dataM_14_1_4)[0])
stepsM_14_2_0 = len(signal.find_peaks(filt_dataM_14_2_0)[0])
stepsM_14_2_5 = len(signal.find_peaks(filt_dataM_14_2_5)[0])
stepsM_14_3_0 = len(signal.find_peaks(filt_dataM_14_3_0)[0])

print(f"Accel-M Steps with 0.5 ms cutoff freq:")
print(f"1.4: {stepsM_05_1_4} |",
      f"2.0: {stepsM_05_2_0} |",
      f"2.5: {stepsM_05_2_5} |",
      f"3.0: {stepsM_05_3_0}")
print()

print(f"Accel-M Steps with 0.8 ms cutoff freq:")
print(f"1.4: {stepsM_08_1_4} |",
      f"2.0: {stepsM_08_2_0} |",
      f"2.5: {stepsM_08_2_5} |",
      f"3.0: {stepsM_08_3_0}")
print()

print(f"Accel-M Steps with 1.0 ms cutoff freq:")
print(f"1.4: {stepsM_10_1_4} |", 
      f"2.0: {stepsM_10_2_0} |",
      f"2.5: {stepsM_10_2_5} |",
      f"3.0: {stepsM_10_3_0}")
print()

print(f"Accel-M Steps with 1.2 ms cutoff freq:")
print(f"1.4: {stepsM_12_1_4} |",
      f"2.0: {stepsM_12_2_0} |",
      f"2.5: {stepsM_12_2_5} |",
      f"3.0: {stepsM_12_3_0}")
print()

print(f"Accel-M Steps with 1.4 ms cutoff freq:")
print(f"1.4: {stepsM_14_1_4} |",
      f"2.0: {stepsM_14_2_0} |",
      f"2.5: {stepsM_14_2_5} |",
      f"3.0: {stepsM_14_3_0}")
print()

# #mt_parser.plot_mt_data(filepath, "Raw Y-Acceleration and PSD plots for 0.5ms stride", "AccY")
# mt_parser.plot_mt_data(filepath_05, "Filtered Y-Acceleration and PSD plots for 0.5ms stride: 1.4Hz cutoff", filt_data_05_1_4)
# mt_parser.plot_mt_data(filepath_05, "Filtered Y-Acceleration and PSD plots for 0.5ms stride: 2.0Hz cutoff", filt_data_05_2_0)
# mt_parser.plot_mt_data(filepath_05, "Filtered Y-Acceleration and PSD plots for 0.5ms stride: 2.5Hz cutoff", filt_data_05_2_5)
# mt_parser.plot_mt_data(filepath_05, "Filtered Y-Acceleration and PSD plots for 0.5ms stride: 3.0Hz cutoff", filt_data_05_3_0)

# mt_parser.plot_mt_data(filepath_05, "Filtered Acceleration and PSD plots for 0.5ms stride: 1.4Hz cutoff", filt_dataM_05_1_4)
# mt_parser.plot_mt_data(filepath_05, "Filtered Acceleration and PSD plots for 0.5ms stride: 2.0Hz cutoff", filt_dataM_05_2_0)
# mt_parser.plot_mt_data(filepath_05, "Filtered Acceleration and PSD plots for 0.5ms stride: 2.5Hz cutoff", filt_dataM_05_2_5)
# mt_parser.plot_mt_data(filepath_05, "Filtered Acceleration and PSD plots for 0.5ms stride: 3.0Hz cutoff", filt_dataM_05_3_0)

# Test Cadence Tracker:
# CT_2_direct = CadenceTracker(freq_Hz = 100, time_window_s = 2)
# CT_3_direct = CadenceTracker(freq_Hz = 100, time_window_s = 4)
# CT_5_direct = CadenceTracker(freq_Hz = 100, time_window_s= 5)

# CT_2_indirect = CadenceTracker(freq_Hz = 100, time_window_s=2, method='indirect')
# CT_3_indirect = CadenceTracker(freq_Hz = 100, time_window_s=4, method='indirect')
# CT_5_indirect = CadenceTracker(freq_Hz = 100, time_window_s=5, method='indirect')

# # Plotting data
# CT_2_Ddata = []
# CT_3_Ddata = []
# CT_5_Ddata = []

# CT_2_Idata = []
# CT_3_Idata = []
# CT_5_Idata = []

# # Calculate cadences .05 for Acc-Y
# step_data = (np.power(data_dict10['AccY'], 2))
# #CT_2_direct.add_datum(step_data)
# #print(f"Steps in CT {CT_2_direct.count_steps()}")
# for idx in range(len(data_dict10['Time_s'])):
#     CT_2_direct.add_measurement(step_data[idx])
#     CT_2_Ddata.append(CT_2_direct.calculate_cadence())

#     CT_3_direct.add_measurement(step_data[idx])
#     CT_3_Ddata.append(CT_3_direct.calculate_cadence())

#     CT_5_direct.add_measurement(step_data[idx])
#     CT_5_Ddata.append(CT_5_direct.calculate_cadence())

#     CT_2_indirect.add_measurement(step_data[idx])
#     CT_2_Idata.append(CT_2_indirect.calculate_cadence())

#     CT_3_indirect.add_measurement(step_data[idx])
#     CT_3_Idata.append(CT_3_indirect.calculate_cadence())

#     CT_5_indirect.add_measurement(step_data[idx])
#     CT_5_Idata.append(CT_5_indirect.calculate_cadence())

# fig, axs = plt.subplots(2,1)
# fig.suptitle("Comparsion of Cadence tracking with 2 second time window")
# axs[0].hlines(target_10, data_dict10['Time_s'][0], data_dict10['Time_s'][-1], label="Target Cadence")
# axs[0].plot(data_dict10['Time_s'], CT_2_Ddata, color="tab:blue", label="Direct Cadence")
# axs[0].legend()
# axs[0].set_ylabel("Cadence (deg/s)")
# axs[0].set_ylim(0, 50)
# axs[1].hlines(target_10, data_dict10['Time_s'][0], data_dict10['Time_s'][-1], label="Target Cadence")
# axs[1].plot(data_dict10['Time_s'], CT_2_Idata, color="tab:orange", label="Indirect Cadence")
# axs[1].legend()
# axs[1].set_xlabel("Time (s)")
# axs[1].set_ylabel("Cadence (deg/s)")
# axs[1].set_ylim(0, 50)

# fig3, axs3 = plt.subplots(2,1)
# fig3.suptitle("Comparsion of Cadence tracking with 3.5 second time window")
# axs3[0].hlines(target_10, data_dict10['Time_s'][0], data_dict10['Time_s'][-1], label="Target Cadence")
# axs3[0].plot(data_dict10['Time_s'], CT_3_Ddata, color="tab:blue", label="Direct Cadence")
# axs3[0].legend()
# axs3[0].set_ylabel("Cadence (deg/s)")
# axs3[0].set_ylim(0, 50)
# axs3[1].hlines(target_10, data_dict10['Time_s'][0], data_dict10['Time_s'][-1], label="Target Cadence")
# axs3[1].plot(data_dict10['Time_s'], CT_3_Idata, color="tab:orange", label="Indirect Cadence")
# axs3[1].legend()
# axs3[1].set_xlabel("Time (s)")
# axs3[1].set_ylabel("Cadence (deg/s)")
# axs3[1].set_ylim(0, 50)

# fig5, axs5 = plt.subplots(2,1)
# fig5.suptitle("Comparsion of Cadence tracking with 5 second time window")
# axs5[0].hlines(target_10, data_dict10['Time_s'][0], data_dict10['Time_s'][-1], label="Target Cadence")
# axs5[0].plot(data_dict10['Time_s'], CT_5_Ddata, color="tab:blue", label="Direct Cadence")
# axs5[0].legend()
# axs5[0].set_ylabel("Cadence (deg/s)")
# axs5[0].set_ylim(0, 50)
# axs5[1].hlines(target_10, data_dict10['Time_s'][0], data_dict10['Time_s'][-1], label="Target Cadence")
# axs5[1].plot(data_dict10['Time_s'], CT_5_Idata, color="tab:orange", label="Indirect Cadence")
# axs5[1].legend()
# axs5[1].set_xlabel("Time (s)")
# axs5[1].set_ylabel("Cadence (deg/s)")
# axs5[1].set_ylim(0, 50)

# plt.subplots_adjust(left=0.1,
#                 bottom=0.1, 
#                 right=0.9, 
#                 top=0.9, 
#                 wspace=0.4, 
#                 hspace=0.6)
# plt.show()