#! /usr/bin/env python3
"""
File for DataQueue Class
"""

# Project Import

# Python Import
from collections import deque
import itertools
import warnings

# 3rd-party import
import numpy as np

class DataQueue():
    """
    FIFO-Queue with ability to return a number of entries based 
    on time window
    """
    def __init__(self, rate_Hz=100, time_limit_s=3, data=None):
        """
        DataQueue Constructor

        Args:
            int rate_Hz - frequency of the incoming data; default 100Hz
            float time_limit_s - Duration of data (in seconds) held be queue
                default 3 seconds
            list data - Initial array; default None
                If data is not None, it is pressumed to be sampled at rate_Hz
                and organized from oldest to newest entry. If data is too 
                large, only the latest 'time_limit_s' duration will be saved
        """
        # Set constants
        self._RATE_HZ = rate_Hz

        # Set 'public' members
        self.time_limit = time_limit_s

        # Set 'private' members
        self._size = int(np.ceil( time_limit_s / (1 / self._RATE_HZ) ))
        if data:
            self._queue = deque(data, maxlen=self._size)
        else:
            self._queue = deque([], maxlen=self._size)



    # Class member properties

    @property
    def RATE_HZ(self):
        """
        Return the current value of RATE_HZ.

        Note: RATE_HZ is a constant and should not be changed
        """
        return self._RATE_HZ

    @property
    def time_limit(self):
        """
        Return the current value of time_limit (sec)
        """
        return self.time_limit

    @time_limit.setter
    def time_limit(self, value):
        """
        Set the current value of time_limit(sec)

        If the current amount of data exceeds the new time limit, only the
        latest that fit in the new duration will be preserved

        Args:
            float value - new time limit in seconds
        """
        self._change_limit(value)

    # Queue Modifiers

    def append(self, mag_val):
        """
        Append new entry to queue
        """
        self._queue.append(mag_val)


    def append_xyz(self, x, y, z):
        """
        Append the magnitude of X, Y, and Z component of new entry

        Args:
            float x
        """
        mag = np.sqrt( np.sum( np.power([x, y, z], 2) ) )
        self._queue.append(mag)


    def _change_limit(self, value):
        """
        Change the time limit 

        If the current amount of data exceeds the new time limit, only the
        latest that fit in the new duration will be preserved
        """
        self._size = int(np.ceil( value / (1 / self._RATE_HZ) ))
        self._queue = deque( self._queue, maxlen=self._size)
        self._time_limit = value


    def _convert_time_to_num(self, time_s):
        """
        Given a number of seconds, return number of element in that duration

        In the case of non-int value, the returned value will be rounded down
        """
        frac = time_s / self._time_limit
        if (frac > 1):
            return self._size
        else:
            return int(self._size*frac)


    def clear(self):
        """
        Clears the queue
        """
        self._queue.clear()


    def get_entries(self, num):
        """
        Return the latest number of entries in the queue
        """
        # Zero Case
        if num == 0:
            return []
        # Too Large Case
        elif num >= len(self._queue):
            warnings.warn("Requested number of entries is larger than queue, \
                          return whole queue", 
                          RuntimeWarning)
            return self._queue.copy()
        # Just Right
        else:
            end_idx = num - len(self._queue)
            self._queue.rotate(end_idx)
            rtn_list = list(itertools.islice(self._queue, 0, num))
            self._queue.rotate(-end_idx)
            return rtn_list
        

    def get_latest_entries(self, time_s):
        """
        Given a number of seconds, return latest element in that duration
        """
        num = self._convert_time_to_num(time_s)
        return get_entries(num)
