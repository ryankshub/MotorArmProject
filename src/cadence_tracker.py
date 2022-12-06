#! /usr/bin/env python3
"""
File for Cadence Tracker Class
"""

# Project Import

# Python Import
from collections import deque
import warnings
# 3rd-party Import
import numpy as np
from scipy import signal

class CadenceTracker():
    """
    Calculates the desired cadence of the arm based on the acceleration 
    readings from the IMU 
    """
    def __init__(self, data_rate_Hz=100, time_window_s=2, method='direct'):
        """
        CadenceTracker Constructer

        Args:
            int data_rate_Hz - frequency of the incoming data; default 100Hz
            float time_window_s - Duration of the data consider; default 2s
                Must be at least 1s
            string method - method for how cadence is calculated
                'direct' - uses internal step counter for cadence
                'indirect' - uses step estimator for cadence
                if an unsupported string is provide, 'direct' is used
        """
        ## Set 'public' members
        self.walking = False

        ## Set 'private' members
        self._DATA_RATE_HZ = data_rate_Hz
        self._TIME_STEP = 1/data_rate_Hz
        self._TIME_WINDOW_S = time_window_s
        if self._TIME_WINDOW_S < 1:
            warnings.warn("WARNING: Time Window too small; adjusting to 1 second", UserWarning)
            self._TIME_WINDOW_S = 1.0

        # Method to count steps
        if not (method == 'direct' or method == 'indirect'):
            raise ValueError("ERROR: Unsupported method provided; please use 'direct' or 'indirect'")
        else:
            self._METHOD = method

        # Set up internal filter:
        self._FILTER_B, self._FILTER_A = signal.butter(3, 2, 'lowpass', fs=self._DATA_RATE_HZ)

        # Non-Const
        self._degree_range = (-1, -1)
        self._steps_per_window = -1
        self._time_to_step = -1

        # Debugging var TODO Remove
        self._step_count = -1

        # Variables for direct counting method
        self._latest_peak = 0
        self._latest_valley = 0
        self._stride_history = deque(maxlen=7)
        

    # Accesser
    @property
    def DATA_RATE(self):
        """
        """
        return self._DATA_RATE_HZ

    @property
    def degree_range(self):
        """
        """
        return self._degree_range

    @property
    def METHOD(self):
        """
        """
        return self._METHOD

    @property
    def steps_per_window(self):
        """
        """
        return self._steps_per_window

    @property
    def time_to_step(self):
        """
        """
        return self._time_to_step

    @property
    def TIME_WINDOW(self):
        """
        """
        return self._TIME_WINDOW_S

    @property
    def step_count(self):
        """
        """
        return self._step_count

    # CadenceTracker fcns
    def cal_degree_range(self, data):
        """
        """
        return -1


    def cal_time_to_step(self, data):
        """
        """
        return -1


    def count_steps(self, data):
        """
        Uses low-pass filter and peak counting to get 
        number of steps in time window

        Rtn:
        int step_count: number of steps detected in data
        """
        filtered_data = signal.filtfilt(self._FILTER_B, self._FILTER_A, data)
        peaks, _ = signal.find_peaks(filtered_data,
                                     distance=40)
        valleys, _ = signal.find_peaks(-filtered_data,
                                        distance=40)

        # First time
        if self._step_count == -1:
            self._latest_peak = peaks[-1]
            self._step_count = len(peaks)

            for i in range(1, len(peaks)):
                stride = (peaks[i] - peaks[i-1])*self._TIME_STEP
                self._stride_history.appendleft(stride)

        # Next Time
        else:
            if peaks[-1] != self._latest_peak - 1:
                # New step found
                if self._latest_peak < self._latest_valley and \
                    peaks[-1] > self._latest_valley:
                    stride = (peaks[-1] - self._latest_peak)*self._TIME_STEP
                    self._stride_history.appendleft(stride)
                    self._step_count += 1
                    self._latest_peak = peaks[-1]
                # Phantom step found, update latest stride length
                elif self._latest_peak > self._latest_valley and \
                    peaks[-1] > self._latest_valley:
                    stride = (peaks[-1] - peaks[-2])*self._TIME_STEP
                    self._stride_history.popleft()
                    self._stride_history.appendleft(stride)
                    self._latest_peak = peaks[-1]
                else:
                    self._latest_peak -= 1
        
        # Update Valley Checkpoint    
        self._latest_valley = valleys[-1]

        # Get steps per window
        s_weights = np.linspace(len(self._stride_history), 1, 
            len(self._stride_history))
        avg_time_btw_step = np.average(self._stride_history, weights=s_weights)

        # Time to end cals
        time_to_end = self._TIME_WINDOW_S - self._latest_peak*self._TIME_STEP
        time_till_step = avg_time_btw_step - time_to_end

        # steps per window
        steps_per_window = (self._TIME_WINDOW_S/avg_time_btw_step) + 1
        
        return steps_per_window
        

    def estimate_steps(self, data):
        """
        Detemines step count estimate by looking at
        dominate freq. 

        Rtn:
        int step_count: number of steps estimated in data
        """
        nPts = len(data)
        f, Pxx = signal.welch(data, self._DATA_RATE_HZ, nperseg=nPts)
        max_idx = np.argmax(Pxx)
        max_freq = f[max_idx]
        if max_freq < .005:
            return 0
        return self._TIME_WINDOW_S / (1/max_freq)


    def update_cadence(self, data):
        """
        """
        if not self.walking:
            # If we are not walking, set values to negative one
            self._degree_range = (-1, -1)
            self._steps_per_window = -1
            self._time_to_step = -1
        else:
            ## UPDATE STEP COUNT
            if (self._METHOD == 'direct'):
                # Directly count the steps
                self._steps_per_window = self.count_steps(data)
            else:
                # Estimate using dominate frequency
                self._steps_per_window = self.estimate_steps(data)

            ## UPDATE TIME TO NEXT STEP
            self._time_to_step = self.cal_time_to_step(data)

            ## UPDATE DEGREE
            self._degree_range = self.cal_degree_range(data)