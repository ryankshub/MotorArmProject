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
        self.modeldata = joblib.load(modelfile)
        # TODO Model Validation

        if threshold > 0 and threshold <= 1:
            self.threshold = threshold
        self.time_window = time_window

        # Set 'private' members
        self._STATE = "unknown"

    # Class member properties
    @property
    def STATE(self):
        """
        """
        return self._STATE

    @property
    def threshold(self):
        """
        """
        return self.threshold

    @threshold.setter
    def threshold(self, value):
        """
        """
        if value > 0 and value <= 1:
            self.threshold = value
        else:
            warnings.warn("Threshold must be a value in range (0,1]; \
                          new value is rejected.",
                          RuntimeWarning)
    
    # Classifier FCNs
    def load_model(self, modelfile):
        """
        """
        self.modeldata = joblib(modelfile)


    def get_model_metrics(self):
        """
        """
        return self.modeldata['metrics']


    def get_model_metadata(self):
        """
        """
        return self.modeldata['metadata']


    def get_model_classifier(self):
        """
        """
        return self.modeldata['modeldata']['classifier']


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
        main_model = self.modeldata['modeldata']['model']
        probs = main_model.predict_prob(feat_df)

        # Threshold and return
        #TODO
        
