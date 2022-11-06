#! /usr/bin/env python3
"""
File for ClassiferSM
"""

# Python imports
import joblib
import warnings

# Project imports

# 3rd-party imports
import numpy as np
import pandas as pd
from scipy import signal, stats


class ClassifierSM:
    """
    """
    def __init__(self, modelfile, threshold=.8, time_window=1.0):
        """
        """
        # Set 'public' members
        self.load_model(modelfile)
        # TODO Model Validation

        # Set up threshold
        self._threshold = threshold
        self.time_window = time_window

        # Set 'private' members
        self._STATE = "unknown"


    # Class member properties
    @property
    def classifier_name(self):
        """
        """
        return self._modeldata['modeldata']['classifier']


    @property
    def STATE(self):
        """
        """
        return self._STATE


    @property
    def model_metadata(self):
        """
        """
        return self._modeldata['metrics']


    @property
    def model_metrics(self):
        """
        """
        return self._modeldata['metrics']


    @property
    def threshold(self):
        """
        """
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        """
        """
        if value > 0 and value <= 1:
            self._threshold = value
        elif value > 1:
            self._threshold = .95
            warnings.warn(f"Threshold must be a value in range (0,1]; \
                          {value} is too high; using .95.",
                          RuntimeWarning)
        else:
            self._threshold = 0
            warnings.warn(f"Threshold must be a value in range (0,1]; \
                          {value} is too low; using 0",
                          RuntimeWarning)
    
    
    # Classifier FCNs
    def load_model(self, modelfile):
        """
        """
        self._modeldata = joblib.load(modelfile)
        self._model = self._modeldata['modeldata']['model']
        self._lables = self._model.classes_


    def predict(self, data, sample_rate=100):
        """
        """
        # Extract features
        feat_dict = {"DomFreq":[], "Intensity":[], "Periodicity":[]}
        nPts = len(data)
        f, Pxx = signal.welch(data, sample_rate, nperseg=nPts)
        max_idx = np.argmax(Pxx)
        feat_dict["DomFreq"].append(f[max_idx])
        feat_dict["Intensity"].append(Pxx[max_idx])
        P_sum = sum(Pxx)
        Pxx_norm = Pxx/P_sum
        feat_dict["Periodicity"].append(stats.entropy(Pxx_norm))
        feat_df = pd.DataFrame(feat_dict)

        # Predict
        probs = self._model.predict_prob(feat_df)[0]
        idx = np.argmax(probs)
        if probs[idx] > self._threshold:
            self._STATE = self._lables[idx]
        else:
            self._STATE = "unknown"

        return self._STATE
        
