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
    magnitude readings from the IMU 
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
        # Set public members
        self.walking = False # True if acceleration data represents walking

        # Set private members
        ## Constants
        self._DATA_RATE_HZ = data_rate_Hz
        self._TIME_STEP = 1/data_rate_Hz
        self._TIME_WINDOW_S = time_window_s
        if self._TIME_WINDOW_S < 1:
            warnings.warn("WARNING: Time Window too small;" 
            "adjusting to 1 second", UserWarning)
            self._TIME_WINDOW_S = 1.0

        ### Method to count steps
        if not (method == 'direct' or method == 'indirect'):
            raise ValueError("ERROR: Unsupported method provided; "
            "please use 'direct' or 'indirect'")
        else:
            self._METHOD = method

        ### Set up internal filter: We use a 3rd-order butterworth with cutoff
        ### freq at 2 Hz 
        self._FILTER_B, self._FILTER_A = signal.butter(3, 2, 
                                                      'lowpass', 
                                                      fs=self._DATA_RATE_HZ)

        ## Non-Constants
        self._steps_per_window = -1 # steps taken during the time window
        self._time_till_step = -1   # time till the next step taken (seconds)
        self._step_count = -1       # number of steps taken during session

        # Variables for direct counting method
        self._latest_peak = 0       # Idx for latest peak in accel data
        self._latest_valley = 0     # Idx for latest valley in accel data
        # history queue of time length between steps
        self._stride_history = deque(maxlen=7) 
        

    ## Properties of Cadence Tracker
    @property
    def DATA_RATE(self):
        """
        Return the rate of the incoming acceleration data
        """
        return self._DATA_RATE_HZ

    @property
    def METHOD(self):
        """
        Returns whether steps are directly counted('direct') or extrapolated 
        from dominant frequency 
        """
        return self._METHOD

    @property
    def steps_per_window(self):
        """
        Returns the number of steps taken in the provided time window

        Updated by the 'update_cadence' method
        """
        return self._steps_per_window

    @property
    def time_till_step(self):
        """
        Returns the estimated number of seconds until the next step

        Updated by the 'update_cadence' method
        """
        return self._time_till_step

    @property
    def TIME_WINDOW(self):
        """
        Returns the length(in seconds) of the time window
        """
        return self._TIME_WINDOW_S

    @property
    def step_count(self):
        """
        Returns the number of steps taken during a session

        Updated by the 'update_cadence' method
        """
        return self._step_count

    ## Private fcns
    def _calc_steps_per_window(self, data):
        """
        Calculates the number of steps taken during the time window as well
        as update the step count and estimate how long until the next step

        Rtn:
        float step_per_window: fractional number of steps detected in data
        """
        # Filter data for steps(peaks) and mid-gait point(valleys)
        filtered_data = signal.filtfilt(self._FILTER_B, self._FILTER_A, data)
        peaks, _ = signal.find_peaks(filtered_data,
                                     distance=40)
        valleys, _ = signal.find_peaks(-filtered_data,
                                        distance=40)

        # First time operations
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

        # Direct counting method
        if self._METHOD == "direct":
            # Get steps per window
            s_weights = np.linspace(len(self._stride_history), 1, 
                len(self._stride_history))
            avg_time_btw_step = np.average(self._stride_history, weights=s_weights)
        
        # Indirect extrapolate method
        else:
            avg_time_btw_step = self._estimate_steps(data)

        # Time to end cals
        time_to_end = self._TIME_WINDOW_S - self._latest_peak*self._TIME_STEP
        self._time_till_step = avg_time_btw_step - time_to_end

        # steps_per_window calc
        self._steps_per_window = (self._TIME_WINDOW_S/avg_time_btw_step)


    def _estimate_steps(self, data):
        """
        Determines the average time between steps by extrapolating from the
        dominant frequency

        Rtn:
        float average time between steps: 1/dominant_frequency
        """
        nPts = len(data)
        f, Pxx = signal.welch(data, self._DATA_RATE_HZ, nperseg=nPts)
        max_idx = np.argmax(Pxx)
        max_freq = f[max_idx]
        if max_freq < .005:
            return (1/.005)
        return (1/max_freq)

    ## Public fcns
    def update_cadence(self, data):
        """
        Given walking data, update the step count, predict the number of 
        seconds till the next step, count/estimate the number of steps taken
        during the time window. 

        If the data is not walking, do not increment the step count and set 
        steps per window and time till next step to -1
        """
        if not self.walking:
            # If we are not walking, set values to negative one
            self._steps_per_window = -1
            self._time_till_step = -1
        else:
            ## UPDATE STEP COUNT
            self._calc_steps_per_window(data)