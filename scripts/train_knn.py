#!/usr/bin/env python3

# Script to produce KNN models

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
def train_knn_model(data_directory, 
    k, 
    plot_feat=False, 
    plot_result=False, 
    binary_class=False):

    # Get Features
    features = build_training_set(data_directory, plot_feat, binary_class)

    # Build Training and Test Data
    train_data, test_data = train_test_split(features, test_size=0.2, random_state=42)
    train_labels = train_data["Label"]
    train_data = train_data.drop(["Label", "EnumLabel"], axis=1)
    test_labels = test_data["Label"]
    test_data = test_data.drop(["Label","EnumLabel"], axis=1)

    # Train Model
    knn_model = KNeighborsClassifier(n_neighbors=k, weights='distance')
    knn_model.fit(train_data, train_labels)

    # Eval Model
    knn_predict = knn_model.predict(test_data)
    knn_accuracy = accuracy_score(np.array(test_labels), np.array(knn_predict))
    print(f"KNN Accuracy: {knn_accuracy}")
    labels = features["Label"].unique()
    knn_confuse_matrix = confusion_matrix(test_labels, knn_predict, labels=labels)
    label_matrix = get_prec_and_recall(knn_confuse_matrix, labels=labels)
    print(f"Confusion Matrix: {knn_confuse_matrix}")
    print(f"Precision/Recall: {label_matrix}")
    # Plot results
    if (plot_result):
        plot_knn_model(knn_model, knn_accuracy, label_matrix)
    
    # Craft model_data
    knn_metrics = {"accuracy":knn_accuracy}

    knn_metadata = {"features":features, 
                    "date":str(datetime.datetime.today()),
                    "version": x_version()}

    knn_modeldata = {"model":knn_model,
                    "classifier":"sklearn.neighbors.KNeighborClassifier"}
    
    knn_dict = {"modeldata":knn_modeldata,
                "metrics":knn_metrics,
                "metadata":knn_metadata}

    print("KNN DICT")
    print(knn_dict)
    return knn_dict


#Explore KKN model
def explore_knn_model(data_directory, 
    K=20, 
    plot_feat=False, 
    plot_result=False, 
    binary_class=False):

    # Get Features
    features = build_training_set(data_directory, plot_feat, binary_class)

    # Build Training and Test Data
    train_data, test_data = train_test_split(features, test_size=0.2, random_state=42)
    train_labels = train_data["Label"]
    train_data = train_data.drop(["Label", "EnumLabel"], axis=1)
    test_labels = test_data["Label"]
    test_data = test_data.drop(["Label","EnumLabel"], axis=1)

    # Explore various models
    knn_candidates = [x for x in range(1,K+1)]
    knn_res = []

    for k in knn_candidates:
        model_cand = KNeighborsClassifier(n_neighbors=k, weights='distance')
        model_cand.fit(train_data, train_labels)
        cand_res = np.array(cross_val_score(model_cand, train_data, train_labels, cv=10))
        print(f"K value: {k:02}, Mean: {cand_res.mean():.4f}, Std dev: {cand_res.std():.4f}")
        knn_res.append(cand_res.mean())
    
    knn_res = np.array(knn_res)
    chosen_k = np.argmax(knn_res) + 1
    print(f"Chosen K: {chosen_k} with {knn_res[chosen_k-1]}")
    # Train Model
    knn_model = KNeighborsClassifier(n_neighbors=chosen_k)
    knn_model.fit(train_data, train_labels)

    # Eval Model
    knn_predict = knn_model.predict(test_data)
    knn_accuracy = accuracy_score(np.array(test_labels), np.array(knn_predict))
    print(f"KNN Accuracy: {knn_accuracy}")
    labels = features["Label"].unique()
    knn_confuse_matrix = confusion_matrix(test_labels, knn_predict, labels=labels)
    label_matrix = get_prec_and_recall(knn_confuse_matrix, labels=labels)
    print(f"Confusion Matrix: {knn_confuse_matrix}")
    print(f"Precision/Recall: {label_matrix}")
    # Plot results
    if (plot_result):
        plot_knn_model(knn_model, knn_accuracy, label_matrix)
    
    # Craft model_data
    knn_metrics = {"accuracy":knn_accuracy}

    knn_metadata = {"features":features, 
                    "date":str(datetime.datetime.today()),
                    "version": x_version()}

    knn_modeldata = {"model":knn_model,
                    "classifier":"sklearn.neighbors.KNeighborClassifier"}
    
    knn_dict = {"modeldata":knn_modeldata,
                "metrics":knn_metrics,
                "metadata":knn_metadata}

    print("KNN DICT")
    print(knn_dict)
    return knn_dict


# Plotting Fcn
def plot_knn_model(model, accuracy, label_matrix):
    # Make Label bar graph
    bar_fig = plt.figure(1)
    bar_fig.suptitle("Precision and Recall for each class", fontsize=24)
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
    width = 0.2
    # Format Bar Graph
    pbar = bar_ax.bar(x=x_axis-width/2, height=precisions, width=width, label="precision")
    rbar = bar_ax.bar(x=x_axis+width/2, height=recalls, width=width, label="recall")

    bar_ax.set_xticks(x_axis)
    bar_ax.set_xticklabels(labels, fontdict={"fontsize": 20})
    bar_ax.set_title(f"KNN w/k={model.n_neighbors} and Acc:{accuracy:.2f}", 
                     fontsize=20)
    bar_ax.legend(fontsize=12)

    bar_ax.bar_label(pbar, fmt='%.2f')
    bar_ax.bar_label(rbar, fmt='%.2f')
    bar_fig.tight_layout()

    plt.show()


# Saving Fcn
def save_knn_model(knn_meta, filename=None):
    if filename is None:
        filename = f"KNN_{str(datetime.datetime.today()).replace(' ','_')}.joblib"
    else:
        filename += ".joblib"
    save_dir = os.path.join(ROOT_PATH, f"models/{filename}")
    joblib.dump(knn_meta, save_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("data_dir", type=str, help="")
    parser.add_argument('-k', type=int, default=3, help="")
    parser.add_argument('-e','--explore', type=int, help="")
    parser.add_argument('-b', '--binary', action='store_true', help="")
    parser.add_argument("-f", "--plot_feats", action='store_true', help="")
    parser.add_argument("-r", "--plot_result", action='store_true', help="")
    parser.add_argument("-s", "--save_model", action='store_true', help="")
    parser.add_argument("-n", "--model_name", type=str, help="")

    args = parser.parse_args()

    
    if args.explore:
        # Explore KNNs
        knn_data = explore_knn_model(args.data_dir, 
            args.explore, 
            args.plot_feats, 
            args.plot_result,
            args.binary)
    else:
        # Train model
        knn_data = train_knn_model(args.data_dir, 
            args.k, 
            args.plot_feats, 
            args.plot_result,
            args.binary)
    # Save model
    if (args.save_model):
        save_knn_model(knn_data, args.model_name)
    
