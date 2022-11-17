#! /usr/bin/env python3
"""
Collection of functions to help massage/manipulate data
"""

# Project import
from .parser_fcns import parse_mt_file, parse_simple_file

# Python import
import os
import re 

# 3rd-party import
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from scipy import signal, stats



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


def build_training_set(data_directory, plot_feat=False, binary_class=False):
    # Parse files
    samples, labels, rates = fill_samples(data_directory)

    # Extract features
    feature_sets = []
    labels_dict = {}
    labels_idx = 0
    for sample, label, fs in zip(samples, labels, rates):
        if binary_class:
            if label != 'walking':
                label = 'ADL'
        if label not in labels_dict:
            labels_dict[label] = labels_idx
            labels_idx += 1
        feature_sets.append(extract_feat(sample, label, labels_dict[label], fs=fs))

    features = pd.concat(feature_sets)

    # Plot features
    if (plot_feat):
        plot_features(features, plot3D=True)

    return features


def extract_feat(samples, label, enum_label, fs=100, entropy=True):
    """
    Given samples, return a labeled training set with features. 
    The feature used are dominant frequency, intensity at dominant freq, and 
    periodicity.  

    Args:
        list of np.arrays samples - list of activity data chunks
        literal label - label of the data.
        int enum_label - numerical representation of the label 
        int fs - sampling frequency of the data 
        bool entropy - defaulted True; if true, uses the entropy of the 
            freq domain to measure periodic characteristic. False results
            in using an in-house measure

    Return:
        Dataframe with four columns: DomFreq, Intensity, Periodicity, Label
    """
    rtn_dict = {"DomFreq":[], "Intensity":[], "Periodicity":[]}
    rtn_dict["Label"] = [label]*len(samples)
    rtn_dict["EnumLabel"] = [enum_label]*len(samples)
    for sample in samples:
        nPts = len(sample)
        f, Pxx = signal.welch(sample, fs, nperseg=nPts)
        max_idx = np.argmax(Pxx)
        rtn_dict["DomFreq"].append(f[max_idx])
        rtn_dict["Intensity"].append(Pxx[max_idx])
        if entropy:
            P_sum = sum(Pxx)
            Pxx_norm = Pxx/P_sum
            rtn_dict["Periodicity"].append(stats.entropy(Pxx_norm))
        else:
            # TO-DO: Add custom spread calculation and compare performance
            # For now make non-entropy calc 0 zero out the Periodicity axis
            rtn_dict["Periodicity"].append(0)

    feat_df = pd.DataFrame(rtn_dict)
    return feat_df


def fill_samples(dir):
    samples = []
    labels = []
    rates = []
    # Read files
    data_files = [f for f in os.listdir(dir) \
        if os.path.isfile(os.path.join(dir, f))]
    for file in data_files:
        if re.match(r"\AMT", file):
            print(f"Dir: {os.path.join(dir, file)}")
            data_dict = parse_mt_file(os.path.join(dir,file))
        elif re.match(r"\ASIM", file):
            print(f"SIM: {os.path.join(dir, file)}")
            data_dict = parse_simple_file(os.path.join(dir,file))
        else:
            raise Exception("Invalid File Format found")
        samples.append(shred_data(data_dict))
        labels.append(str.lower(data_dict['Action']))
        rates.append(data_dict['SampleRate'])
    return samples, labels, rates


def get_prec_and_recall(label_matrix, labels):
    metric_dict = {}
    elems_predicted = label_matrix.sum(0)
    elems_totals = label_matrix.sum(1)

    for i in range(len(labels)):
        precision = 0
        recall = 0
        true_pos = label_matrix[i][i]
        elems_found = elems_predicted[i]
        elem_total = elems_totals[i]

        if elem_total == 0:
            metric_dict[labels[i]] = (0.0,0.0,False)
            continue
        if elems_found > 0:
            precision = true_pos/elems_found
        if elem_total > 0:
            recall = true_pos/elem_total

        metric_dict[labels[i]] = (precision, recall, True)
    
    return metric_dict


def plot_features(features, plot3D=True):
    label_vals = features["Label"].unique()
    # Set up Figures and Axes
    fig1 = plt.figure(1)
    fig1.suptitle("Feature Figure 1")
    fig2 = plt.figure(2)
    fig2.suptitle("Feature Figure 2")
    fig3 = plt.figure(3)
    fig3.suptitle("Feature Figure 3")

    # Axes 1
    ax1 = fig1.add_subplot(111)
    ax1.set_xlabel("Frequency[Hz]")
    ax1.set_ylabel("Intensity")
    ax1.set_title("Dominant Frequency vs Dominant Intensity")

    # Axes 2
    ax2 = fig2.add_subplot(111)
    ax2.set_xlabel("Intensity")
    ax2.set_ylabel("Periodicity")
    ax2.set_title("Dominant Intensity vs Periodicity")

    # Axes 3
    ax3 = fig3.add_subplot(111)
    ax3.set_xlabel("Frequency[Hz]")
    ax3.set_ylabel("Periodicity")
    ax3.set_title("Dominant Frequency vs Periodicity")


    for label_val in label_vals:
        subset_df = features[features['Label'] == label_val]
        # Figure 1 DomFreq v Intensity
        ax1.scatter(x=subset_df["DomFreq"],
                    y=subset_df["Intensity"],
                    label=label_val)
        
        # Figure 2 Intensity vs Entropy
        ax2.scatter(x=subset_df["Intensity"],
                    y=subset_df["Periodicity"],
                    label=label_val)

        # Figure 3 DomFreq vs Entropy
        ax3.scatter(x=subset_df["DomFreq"],
                    y=subset_df["Periodicity"],
                    label=label_val)
    ax1.legend()
    ax2.legend()
    ax3.legend()
    
    if (plot3D):
        fig4 = plt.figure(4)
        fig4.suptitle("Activity Feature Space")
        ax4 = fig4.add_subplot(111, projection='3d')
        for label_val in label_vals:
            subset_df = features[features['Label'] == label_val]
            ax4.scatter(xs=subset_df["DomFreq"],
                        ys=subset_df["Intensity"],
                        zs=subset_df["Periodicity"],
                        label=label_val)

        ax4.set_xlabel("Frequency[Hz]")
        ax4.set_ylabel("Intensity")
        ax4.set_zlabel("Periodicity")
        ax4.legend()

    plt.show()


def shred_data(data_dict, samples=None, interval=3.0, time_key="Time_s", data_key="AccM"):
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
    final_time = data_dict[time_key][-1]
    idx = 0
    curr_time = data_dict[time_key][idx]
    rtn_array = []
    while (final_time - curr_time) > interval:
        next_time = curr_time
        next_idx = idx
        curr_sample = []
        # Make shred
        while (next_time - curr_time) < interval:
            curr_sample.append(data_dict[data_key][next_idx])
            next_idx += 1
            next_time = data_dict[time_key][next_idx]
        # Save shred
        s_arry = np.array(curr_sample)
        rtn_array.append(s_arry)
        idx += 1
        curr_time = data_dict[time_key][idx]

    if samples is not None:
        rtn_array = samples + rtn_array
    
    return rtn_array
