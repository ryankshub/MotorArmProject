#! /usr/bin/env python3

# Project Import

# Python Import

# 3rd-party Import
import numpy as np

class CadenceTracker():
    """
    Calculates the desired cadence of the arm based on the acceleration 
    readings from the IMU 
    """
    def __init__(self, freq_Hz=100, time_window_ms=100, data=None):
        """
        CadenceTracker Constructer

        Args:
            number freq_Hz - frequency of the incoming data; default 100Hz
            int time_window_ms - Duration of the data consider; default 100ms
            list data - Initial dataset; default None
        """
        # Calculate size of data array based on time window and freq
        self._freq_Hz = freq_Hz
        self._time_window_ms = time_window_ms
        self._size = int(np.ceil(time_window_ms / (1000 / self._freq_Hz)))
        self._data = np.array([], dtype=np.float64)
        # Input initial data, only keep 'size' latest values
        if(data):
            self._data = np.append(self._data, data)
        if(len(self._data) > self._size):
            self._data = np.delete(self._data, np.s_[0:len(self._data)-self._size])
        # Set initial cadence
        self._target_cadence_rads = 0.0


    def clear_data(self):
        """
        Clears tracker of acceleration data
        """
        self._data = np.array([], dtype=float64)


    def add_measurement(self, accel_val):
        """
        Add 1 acceleration measurement to tracker. If window is full, 
        this will also remove oldest data point

        Args:
            number accel_val - latest acceleration measurement (m/s)
        """
        self._data = np.append(self._data, accel_val)
        if (self._data > self._size):
            self._data = np.delete(self._data, 0)


    def add_datum(self, accel_vals):
        """
        Add multiple measurement values to trackers. If window is full, 
        the tracker will only keep the latest values
        Args:
            list accel_vals - latest acceleration measurements (m/s)
        """

        self._data = np.append(self._data, accel_vals)
        if (self._data > self._size):
            self._data = np.delete(self._data, np.s_[0:len(self._data) - self.size])

    
    def find_step(self, idx):
        """
        Search for step in data starting from idx
        """
        pass


    def calculate_cadence(self):
        """
        Return the estimated cadence the arm should take in rads 
        """
        return self._target_cadence 


    



        