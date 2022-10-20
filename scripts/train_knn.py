#!/usr/bin/env python3

# Script to produce KNN models

#Python imports
import argparse
from curses import meta
import joblib
import os
import sys

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from utils import build_training_set, get_prec_and_recall
# plot_features

# 3rd-party Import
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


# Training Fcn
def train_knn_model(data_directory, k, plot_feat=False, plot_result=False):
    # Get Features
    features = build_training_set(data_directory, plot_feat)

    # Build Training and Test Data
    train_data, test_data = train_test_split(features, test_size=0.2, random_state=42)
    train_labels = train_data["Label"]
    train_data = train_data.drop(["Label"], axis=1)
    test_labels = test_data["Label"]
    test_data = test_data.drop(["Label"], axis=1)

    # Train Model
    knn_model = KNeighborsClassifier(n_neighbors=k)
    knn_model.fit(train_data, train_labels)

    # Eval Model
    knn_predict = knn_model.predict(test_data)
    knn_accuracy = accuracy_score(np.array(test_labels), np.array(knn_predict))
    print(f"KNN Accuracy: {knn_accuracy}")
    labels = features["Label"].unique()
    knn_confuse_matrix = confusion_matrix(test_labels, knn_predict, labels=labels)
    label_matrix = get_prec_and_recall(knn_confuse_matrix, labels=labels)

    # Plot results
    if (plot_result):
        plot_knn_model(knn_model, knn_accuracy, label_matrix)
    
    return knn_model, knn_accuracy, features


# Plotting Fcn
def plot_knn_model(model, accuracy, label_matrix):
    # Make Label bar graph
    bar_fig = plt.figure(1)
    bar_fig.suptitle("Precision and Recall for each class")
    bar_ax = bar_fig.add_subplot(111)
    labels = []
    precisions = []
    recalls = []
    # Loop to get data from matrix
    for label in label_matrix:
        precision, recall, exist = label_matrix[label]
        if not exist:
            continue
        else:
            labels.append(label)
            precisions.append(precision)
            recalls.append(recall)
    
    x_axis = np.arange(len(labels))

    bar_ax.bar(x=x_axis-0.2, height=precisions, width=0.4, label="precision")
    bar_ax.bar(x=x_axis+0.2, height=recalls, width=0.4, label="recall")
    bar_ax.set_xlabel("Activities")
    bar_ax.set_xticks(labels)
    bar_ax.set_title(f"KNN w/k={model.n_neighbor} and Acc:{accuracy}")
    bar_ax.legend()
    plt.show()


# Saving Fcn
def save_knn_model(metadata, save_dir=None, filename=None):
    if filename is None:
        filename = "KNN.joblib"
    if save_dir is None:
        save_dir = os.path.join(ROOT_PATH, f"models/{filename}")
    joblib.dump(metadata, save_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("data_dir", type=str, help="")
    parser.add_argument('-k', type=int, default=3, help="")
    parser.add_argument("--plot_feats", "-f", action='store_true', help="")
    parser.add_argument("--plot_result", "-r", action='store_true', help="")

    args = parser.parse_args()

    # Train model
    model = train_knn_model(args.data_dir, args.k, args.plot_feats, args.plot_result)
    # Save model
    
