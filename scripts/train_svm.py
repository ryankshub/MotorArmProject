#!/usr/bin/env python3

# Script to produce SVM models

#Python imports
import argparse
import datetime
import joblib
import os
import sys

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from utils import build_training_set, get_prec_and_recall, x_version

# 3rd-party Import
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

#Training Fcn
def train_svm_model():
    pass