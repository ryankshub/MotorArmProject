#! /usr/bin/env python3
"""
File for Classifer State Machine Class
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
    Classifier state machine that identifies which activity acceleration data
    represents
    """
    def __init__(self, modelfile, threshold=.8, time_window=1.0):
        """
        Constructor of Classifier State Machine

        Args:
            string modelfile - a joblib binary that contains the classifier 
                information. The infomation should contain the modeldata with 
                the model and type of classifier, a dictionary of metrics 
                (e.g. accuracy) of the model, and metadata contain the training
                features, date generated, and version of this software used to 
                generate it. 
            float threshold - the minimum confidence the classifier must have 
                for predicting a state
            float time_window - length of input data in number of seconds
        """
        # Set public members
        self.time_window = time_window

        ## Set up threshold
        self.threshold = threshold

        # Set private members
        ## Load model file TODO Model Validation
        self.load_model(modelfile)

        ## Set Constants
        self._STILL_STATE = "waiting"
        self._STILL_STATE_THRES = 0.2 # minimum signal power to classify
        # state when classification confidence is below threshold
        self._UNKNOWN_STATE = "unknown" 
        self._STATE = self._UNKNOWN_STATE


    # ClassifierSM properties
    @property
    def classifier_name(self):
        """
        Return the name of the classifier loaded
        """
        return self._modeldata['modeldata']['classifier']

    @property
    def model_metadata(self):
        """
        Return a dictionary with the training features used by the model, the 
        date the model was generated, and the software version when it was 
        generated
        """
        return self._modeldata['metadata']


    @property
    def model_metrics(self):
        """
        Return a dictionary of model metrics
        """
        return self._modeldata['metrics']

    @property
    def STATE(self):
        """
        Return the current state
        """
        return self._STATE

    @property
    def threshold(self):
        """
        Return the current threshold
        """
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        """
        Updates the threshold value. Threshold should be in the range (0,1]; if
        threshold is too low, it is set to .01. If it is too high, it is set to 
        .95
        """
        if value > 0 and value <= 1:
            self._threshold = value
        elif value > 1:
            self._threshold = .95
            warnings.warn(f"Threshold must be a value in range (0,1]; \
                          {value} is too high; using .95.",
                          RuntimeWarning)
        else:
            self._threshold = .01
            warnings.warn(f"Threshold must be a value in range (0,1]; \
                          {value} is too low; using 0",
                          RuntimeWarning)
    
    
    # Public fcns
    def load_model(self, modelfile):
        """
        Load a modelfile into the state machine

        Args:
            string modelfile - a joblib binary that contains the classifier 
                information.
        """
        self._modeldata = joblib.load(modelfile)
        self._model = self._modeldata['modeldata']['model']
        self._lables = self._model.classes_


    def predict(self, data, sample_rate=100):
        """
        Predict which activity the data represents and update the state 
        accordingly

        Args:
            list-like data - array of acceleration magnitude time-series
            num sample_rate - sample rate of items in data
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
        probs = self._model.predict_proba(feat_df)[0]
        idx = np.argmax(probs)
        if feat_dict["Intensity"][0] < self._STILL_STATE_THRES:
            self._STATE = self._STILL_STATE_THRES
        elif probs[idx] > self._threshold:
            self._STATE = self._lables[idx]
        else:
            self._STATE = self._UNKNOWN_STATE

        return self._STATE
        
