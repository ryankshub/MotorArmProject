#!/usr/bin/env python3

# Script to produce KNN models

#Python import
import argparse
import os
import sys

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from utils import build_training_set
# plot_features

# 3rd-party Import
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier as knnC


# Training Fcn
def train_knn_model(data_directory, plot_feat=False, plot_result=False, **model_args):
    # Get Features
    features = build_training_set(data_directory, plot_feat)

    # Train models
    train_data, test_data = train_test_split(features, test_size=0.9, random_state=42)
    train_labels = train_data["Label"]
    train_data = train_data.drop(["Label"], axis=1)
    test_labels = test_data["Label"]
    test_data = test_data.drop(["Label"], axis=1)


    # knn_model = knnC(n_neighbors=3)
    # knn_model.fit(train_data, train_labels)
    # knn_predict = knn_model.predict(test_data)
    # knn_accuracy = accuracy_score(np.array(test_labels), np.array(knn_predict))
    # print(f"KNN Accuracy: {knn_accuracy}")

    # Plot results
    if (plot_result):
        plot_knn_model(knn_model, test_labels)
    
    return knn_model


# Plotting Fcn
def plot_knn_model(model):
    print("Insert Graph Homie")


# Saving Fcn
def save_knn_model(model, save_dir, filename=None):
    print("Saving Model Homie")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("train_dir", type=str, help="")
    parser.add_argument("--plot_feats", "-f", action='store_true', help="")
    parser.add_argument("--plot_result", "-r", action='store_true', help="")

    args = parser.parse_args()

    # Train model
    model = train_knn_model(args.train_dir, args.plot_feats, args.plot_result)
    # Save model
    
