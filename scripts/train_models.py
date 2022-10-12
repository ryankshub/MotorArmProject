#!/usr/bin/env python3

# Machine Learning Pipeline

#Python import
import argparse
import os
import re
import sys
import time

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from utils import extract_feat, parse_mt_file, shred_data
# plot_features

# 3rd-party Import
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Available Models bit-flag
KNN = 0b00001
SVM = 0b00010
MULTI_LINEAR = 0b00100
RADIX_SVM = 0b01000
POLY_SVM = 0b10000

# Training pipeline
def train_models(train_directory, models_bit_flag, plot_feat=False, plot_result=False):
    # Set model bools
    train_knn = KNN & models_bit_flag
    train_svm = SVM & models_bit_flag
    train_mul_lin = MULTI_LINEAR & models_bit_flag
    train_radix_svm = RADIX_SVM & models_bit_flag
    train_poly_svm = POLY_SVM & models_bit_flag
    print(f"Dir {train_directory}")

    print(f"KNN: {train_knn}")
    print(f"SVM: {train_svm}")
    print(f"MULTI: {train_mul_lin}")
    print(f"RADIX: {train_radix_svm}")
    print(f"POLY: {train_poly_svm}")

    # Set up file paths
    walk_path = os.path.abspath(os.path.join(train_directory, 'walk'))
    print(os.listdir(walk_path))
    print(f"Walk Path: {walk_path}")
    walk_files = get_files_in_dir(walk_path)
    print(f"Walk Files: {walk_files}")
    non_walk_path = os.path.abspath(os.path.join(train_directory, 'non_walk'))
    print(f"Non Walk Path: {non_walk_path}")
    non_walk_files = get_files_in_dir(non_walk_path)
    print(f"Non Walk Files: {non_walk_files}")

    # Parse walking files
    walk_samples = fill_samples(walk_path, walk_files)
    print("Walk Samples")
    print(walk_samples[5])
    # non_walk_path = fill_samples(non_walk_files)

    # # Extract features
    # walk_features = extract_feat(walk_samples, label=1)
    # non_walk_features = extract_feat(non_walk_features, label=0)
    # features = pd.concat([walk_features, non_walk_features]) 

    # # Plot features
    # if (plot_feat):
    # plot_features(walk_features, non_walk_features)

    # Train models
     

def get_files_in_dir(dir_path):
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    return files


def fill_samples(dir, files):
    samples = []
    for file in files:
        if re.match(r"\AMT", file):
            data_dict = parse_mt_file(os.path.join(dir,file))
            print("AccelerationM")
            print(data_dict["AccM"][:100])
        #TODO: Add other parsers
        # elif re.match(r"\ASIM", filename):
        #     data_dict = parse_simple_file(file)
        # elif re.match(r"\AIMU", filename):
        #     data_dict = parse_imu_file(file)
        else:
            raise Exception("Invalid File Format found")
        samples = shred_data(data_dict, samples=samples)
    return samples


def plot_features(walk_feats, non_walk_feats, plot_3D=True):
    # Figure 1 DomFreq v Intensity
    plt.figure(1)
    plt.scatter(x=walk_feats["DomFreq"], 
                y=walk_feats["Intensity"],
                c="blue",
                label="Walk")
    plt.scatter(x=non_walk_feats["DomFreq"],
                y=non_walk_feats["Intensity"],
                c="red",
                label="Non-walk")
    plt.xlabel("Dominant Frequency[Hz]")
    plt.ylabel("Intensity")

    # Figure 2: Intensity vs Entropy
    plt.figure(2)
    plt.scatter(x=walk_feats["Intensity"],
                y=walk_feats["Periodicity"],
                c="blue",
                label="Walk")
    plt.scatter(x=non_walk_feats["Intensity"],
                y=non_walk_feats["Periodicity"],
                c="red",
                label="Non-walk")
    plt.xlabel("Intensity")
    plt.ylabel("Entropy")

    # Figure 3: DomFreq vs Entropy
    plt.figure(3)
    plt.scatter(x=walk_feats["DomFreq"],
                y=walk_feats["Periodicity"],
                c="blue",
                label="Walk")
    plt.scatter(x=non_walk_feats["DomFreq"],
                y=non_walk_feats["Periodicity"],
                c="red",
                label="Non-walk")
    plt.xlabel("Dominant Frequency[Hz]")
    plt.ylabel("Entropy")

    
    if (plot_3D):
        fig = plt.figure(4)
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xs=walk_feats['DomFreq'],
                   ys=walk_feats['Intensity'],
                   zs=walk_feats['Periodicity'],
                   c="blue",
                   label="Walk")
        ax.scatter(xs=non_walk_feats['DomFreq'],
                   ys=non_walk_feats['Intensity'],
                   zs=non_walk_feats['Periodicity'],
                   c="red",
                   label="Non-walk")
        ax.xlabel("Dominant Frequency[Hz]")
        ax.ylabel("Intensity")
        ax.zlabel("Periodicity")

    plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("train_dir", type=str, help="")
    parser.add_argument("--knn", "-k", action='store_true', help="")
    parser.add_argument("--svm", "-s", action='store_true', help="")
    parser.add_argument("--multi_linear", "-l", action='store_true', help="")
    parser.add_argument("--radix_svm", "-x", action='store_true', help="")
    parser.add_argument("--poly_svm", "-p", action='store_true', help="")
    parser.add_argument("--plot_feats", "-f", action='store_true', help="")
    parser.add_argument("--plot_result", "-r", action='store_true', help="")

    args = parser.parse_args()
    models = [args.knn, args.svm, args.multi_linear, args.radix_svm, args.poly_svm]
    bit_flag = 0
    for i in range(len(models)):
        bit_flag |= (models[i] << i)
    print(f"Bit Flag {bin(bit_flag)}")
    train_models(args.train_dir, bit_flag, args.plot_feats, args.plot_result)


