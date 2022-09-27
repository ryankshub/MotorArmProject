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

def shred_data(data_dict, samples=None, interval=3.5, time_key="TimeS", data_key="AccM"):
    """
    Convert time series data into shreds of interval length. 
    Shreds are arrays with all data within one interval of current timestep

    Args:
        dict/DataFrame data_dict - dictionary containing data to be shredded. Should have
            a time series corresponding to the data. This fcn assumes time is
            measured in seconds
        list of np.arrays samples - previous list to include in results
        float interval - how long, in seconds, each shred should be
        literal time_key - Key to access time series in data_dict
        literal data_key - Key to access data series in data_dict

    Returns
        List of shreds(np.array). If samples is not None, the returned list
        will have samples prepended to the results. e.g.
        results = samples + new shreds
    """
    pass

def extract_feat(samples, label, entropy=True):
    """
    Given samples, return a labeled training set with features. 
    The feature used are dominant frequency, intensity at dominant freq, and 
    periodicity.  

    Args:
        list of np.arrays samples - list of activity data chunks
        literal label - label of the data. 
        bool entropy - defaulted True; if true, uses the entropy of the 
            freq domain to measure periodic characteristic. False results
            in using an in-house measure

    Return:
        Dataframe with four columns: DomFreq, Intensity, Periodicity, Label
    """
    pass 
