#! /usr/bin/env python3
"""
Collection of functions to help massage/manipulate data
"""

# Project import

# Python import

# 3rd-party import
from scipy import signal

def apply_filter(data, fs, filter_order, filter_type, cutoff_freq):
    """
    Apply butterworth filter of certain type

    Args:
        np.array data - raw data
        float fs - sampling frequency
        int filter_order - order of the butterworth filter
        string filter_type - type of filter: options are 'lowpass', 'highpass',
            'bandpass', or 'bandstop' 
        float(s) cutoff_freq - cutoff frequency for the filter. For 'lowpass' 
            and 'highpass' should be a scalar; for 'bandpass' or 'bandstop', the 
            frequency should be a two-elem list
    """
    b, a = signal.butter(filter_order, cutoff_freq, filter_type, fs=fs)
    return signal.lfilter(b, a, data)

def apply_zero_phase_filter(data, fs, filter_order, filter_type, cutoff_freq):
    """
    Apply butterworth filter of certain type twice; once forward and once backward. 
    This filtering method is NOT causal

    Args:
        np.array data - raw data
        float fs - sampling frequency
        int filter_order - order of the butterworth filter
        string filter_type - type of filter: options are 'lowpass', 'highpass',
            'bandpass', or 'bandstop' 
        float(s) cutoff_freq - cutoff frequency for the filter. For 'lowpass' 
            and 'highpass' should be a scalar; for 'bandpass' or 'bandstop', the 
            frequency should be a two-elem list
    """
    b, a = signal.butter(filter_order, cutoff_freq, filter_type, fs=fs)
    return signal.filtfilt(b, a, data)