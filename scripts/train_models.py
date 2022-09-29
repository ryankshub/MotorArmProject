#!/usr/bin/env python3

# Machine Learning Pipeline

#Python import
import argparse
import os
import sys
import time

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project Import
from utils import extract_feat, parse_mt_file, shred_data

# 3rd-party Import
import matplotlib.pyplot as plt

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

    # Set up file paths
    walk_path = os.path.join(train_directory, 'walk')
    non_walk_path = os.path.join(train_directory, 'non_walk')

    # Parse walking files
    walk_samples = fill_samples(walk_path)
    non_walk_path = fill_samples(non_walk_path)

    # Extract features
    walk_features = extract_feat(walk_samples, label=1)
    non_walk_features = extract_feat(non_walk_features, label=0)

    # Plot features

    # Train models
     
        

def fill_samples(directory):
    samples = []
    for file in directory:
        if regex_check for MT:
            data_dict = parse_mt_file(file)
        else:
            raise Exception e("Invalid File Format found")
        samples = shred_data(data_dict, samples=samples)
    return samples


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("train_dir", type=str, help="")
    parser.add_argument("--knn", type=bool, help="")
    parser.add_argument("--svm", type=bool, help="")
    parser.add_argument("--multi_linear", type=bool, help="")
    parser.add_argument("--radix_svm", type=bool, help="")
    parser.add_argument("--poly_svm", type=bool, help="")
    parser.add_argument("--plot_feats", "-f", type=bool, help="")
    parser.add_argument("--plot_result", "-r", type=bool, help="")

    args.parser.parse_args()
    model


