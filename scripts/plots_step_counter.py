#! /usr/bin/env python3

# Plots bar graph of steps data

# Python imports

# Project imports

# 3rd-Party imports
import matplotlib.pyplot as plt 

cutoff_freqs = [1.4, 2.0, 2.5, 3.0]

values_05 = [46, 66, 81, 90]
target_05 = 35

values_08Y = [50, 51, 64, 90]
values_08 = [50, 51, 59, 84]
target_08 = 50

values_10 = [52, 52, 52, 64]
target_10 = 52

values_12 = [57, 57, 57, 58]
target_12 = 57

values_14 = [60, 61, 61, 61]
target_14 = 60

fig1, ax1 = plt.subplots(2, 2)

fig1.suptitle("Estimating number of steps after filtering raw data for Accel-M")

ax1[0][0].set_title("Estimated 0.8 m/s")
ax1[0][0].bar(cutoff_freqs, values_08, width=0.1, color='b')
ax1[0][0].set_xlabel("Cutoff Freq [Hz]")
ax1[0][0].set_ylabel("Steps Count")
ax1[0][0].hlines(target_08, xmin=0, xmax=3.2,colors='r')

ax1[0][1].set_title("Estimated 1.0 m/s")
ax1[0][1].bar(cutoff_freqs, values_10, width=0.1, color='b')
ax1[0][1].set_xlabel("Cutoff Freq [Hz]")
ax1[0][1].set_ylabel("Steps Count")
ax1[0][1].hlines(target_10, xmin=0, xmax=3.2,colors='r')

ax1[1][0].set_title("Estimated 1.2 m/s")
ax1[1][0].bar(cutoff_freqs, values_12, width=0.1, color='b')
ax1[1][0].set_xlabel("Cutoff Freq [Hz]")
ax1[1][0].set_ylabel("Steps Count")
ax1[1][0].hlines(target_12, xmin=0, xmax=3.2,colors='r')

ax1[1][1].set_title("Estimated 1.4 m/s")
ax1[1][1].bar(cutoff_freqs, values_14, width=0.1, color='b')
ax1[1][1].set_xlabel("Cutoff Freq [Hz]")
ax1[1][1].set_ylabel("Steps Count")
ax1[1][1].hlines(target_14, xmin=0, xmax=3.2,colors='r')

plt.show()

