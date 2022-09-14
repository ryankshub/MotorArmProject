#! /usr/bin/env python3
"""
File for Cadence Tracker Class
"""

# Project Import

# Python Import
from collections import deque
# 3rd-party Import
import numpy as np
from scipy import signal

class CadenceTracker():
    """
    Calculates the desired cadence of the arm based on the acceleration 
    readings from the IMU 
    """
    def __init__(self, freq_Hz=100, time_window_s=2, data=None, method='direct'):
        """
        CadenceTracker Constructer

        Args:
            int freq_Hz - frequency of the incoming data; default 100Hz
            float time_window_s - Duration of the data consider; default 2s
                Must be at least 1s
            list data - Initial dataset; default None
            string method - method for how cadence is calculated
                'direct' - uses internal step counter for cadence
                'indirect' - uses step estimator for cadence
                if an unsupported string is provide, 'direct' is used
        """
        # Calculate size of data array based on time window and freq
        self._freq_Hz = freq_Hz
        self._time_window_s = time_window_s
        if self._time_window_s < 1:
            print("WARNING: Time Window too small; adjusting to 1 second")
            self._time_window_s = 1.0
        self._size = int(np.ceil(time_window_s / (1 / self._freq_Hz)))
        self._min_size = int(np.ceil(self._size/time_window_s))
        self._data = np.array([], dtype=np.float64)

        # Input initial data, only keep 'size' latest values
        if(data):
            self._data = np.append(self._data, data)
        if(len(self._data) > self._size):
            self._data = np.delete(self._data, np.s_[0:len(self._data)-self._size])

        # Initial Cadence weighted average window
        self._HISTORY_SIZE = 15
        self._cadence_history = deque([0.0]*self._HISTORY_SIZE, maxlen=self._HISTORY_SIZE)
        self._cadence_weights = [i+1 for i in range(self._HISTORY_SIZE)]

        # Max degree arc TODO: Calculate this as it may change based on speed
        self._DEGREES_PER_STEP = 20.0
        self._method = 'direct'
        if not (method == 'direct' or method == 'indirect'):
            print("WARNING: Unsupported method provided; using direct")
        else:
            self._method = method
        # Set up internal filter:
        self._FILTER_B, self._FILTER_A = signal.butter(3, 2, 'lowpass', fs=self._freq_Hz)


    def clear_data(self):
        """
        Clears tracker of acceleration data
        """
        self._data = np.array([], dtype=np.float64)


    def add_measurement(self, accel_val):
        """
        Add 1 acceleration measurement to tracker. If window is full, 
        this will also remove oldest data point

        Args:
            number accel_val - latest acceleration measurement (m/s)
        """
        self._data = np.append(self._data, accel_val)
        if (len(self._data) > self._size):
            self._data = np.delete(self._data, 0)


    def add_datum(self, accel_vals):
        """
        Add multiple measurement values to trackers. If window is full, 
        the tracker will only keep the latest values
        Args:
            list accel_vals - latest acceleration measurements (m/s)
        """

        self._data = np.append(self._data, accel_vals)
        if (len(self._data) > self._size):
            print("LOST DATA")
            self._data = np.delete(self._data, np.s_[0:len(self._data) - self._size])


    def count_steps(self):
        """
        Uses low-pass filter and peak counting to get 
        number of steps in time window

        Rtn:
        int step_count: number of steps detected in data
        """
        filtered_data = signal.lfilter(self._FILTER_B, self._FILTER_A, self._data)
        step_count = len(signal.find_peaks(filtered_data)[0])
        return step_count
        

    def estimate_steps(self):
        """
        Detemines step count estimate by looking at
        dominate freq. 

        Rtn:
        int step_count: number of steps estimated in data
        """
        nPts = len(self._data)
        f, Pxx = signal.welch(self._data, self._freq_Hz, nperseg=nPts)
        max_idx = np.argmax(Pxx)
        max_freq = f[max_idx]
        return np.ceil(self._time_window_s / (1/max_freq))


    def calculate_cadence(self):
        """
        Return the estimated cadence the arm should take in deg/s
        """
        # We need at least a second of data for accurate cadence count
        if (len(self._data) < self._min_size):
            return 0.0

        # Try to estimate with smaller window if not full
        # time_collected = self._time_window_s
        
        # if ((len(self._data) < self._size) and (self._method == 'direct')):
        #     time_collected = (len(self._data)/self._size)*self._time_window_s
        
        # Pick which method to get step counts
        step_count = 0
        if (self._method == 'direct'):
            # Apply sliding window for direct step method
            step_count = self.count_steps() 
        elif (self._method == 'indirect'):
            step_count = self.estimate_steps()
        else:
            #TODO: Throw exception?
            print("ERROR: UNSUPPORTED STEP COUNT METHOD FOUND")
            step_count = 0
        # Convert step count to cadence
        # arc_length = self._DEGREES_PER_STEP * step_count
        # target_cadence_degs = arc_length / time_collected

        # Add cadence to rolling weighted average
        # self._cadence_history.append(target_cadence_degs)
        # rtn_cadence = np.average(self._cadence_history, weights=self._cadence_weights)
        return step_count