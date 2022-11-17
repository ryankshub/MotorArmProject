#! /usr/bin/env python3

## Test file for imports

import os
import sys
FILE_PATH = sys.path[0]
print(FILE_PATH)
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)
print(sys.path)

import src
print(src)
import utils
print(utils)

import argparse
import joblib
import pandas as pd
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is a simple test file for rough code")
    parser.add_argument("-f","--test_file", type=str, help="")
    parser.add_argument("-d","--test_dir", type=str, help="")
    
    args = parser.parse_args()
    # dic = utils.parse_simple_file(args.test_file)
    # print(f"Action: {dic['Action']}")
    # print(f"SampleRate: {dic['SampleRate']}")
    # print(f"Timestamps: {dic['Time_s'][:10]}")
    # print(f"AccX: {dic['AccX'][:10]}")
    # print(f"AccY: {dic['AccY'][:10]}")
    # print(f"AccZ: {dic['AccZ'][:10]}")
    # filepath = None
    # if args.test_file is not None:
    #     filepath = os.path.join(ROOT_PATH, args.test_file)
    #     dic = utils.parse_mt_file(filepath)

    #     print(f"File {filepath}")
    #     print(f"Action: {dic['Action']}")
    #     print(f"Sample Rate: {dic['SampleRate']}")
    #     print("Time Sample")
    #     print(dic["Time_s"][:15])
    #     print("Acceleration Sample")
    #     print(dic["AccX"][:15])

    filedir = None
    if args.test_dir is not None:
        filedir = args.test_dir
        features = utils.build_training_set(filedir, plot_feat=True, binary_class=False)
        # print(features[['DomFreq', "Intensity"]])

    # test_row = [1.714286, 4.534283, 2.220323]
    # test_dict = {"DomFreq":[1.8], "Intensity":[2], "Periodicity":[2.2]}
    # df = pd.DataFrame(test_dict)
    # print("Loading KNN Model")
    # knn_data = joblib.load(os.path.join(ROOT_PATH, "models","Zesty_Knn.joblib"))
    # knn_modeldata = knn_data['modeldata']
    # knn_metrics = knn_data['metrics']
    # print(f"Acc: {knn_metrics['accuracy']}")
    # print(knn_modeldata)
    # knn_model = knn_modeldata["model"]
    # print(knn_model.feature_names_in_)
    # lbls = knn_model.classes_
    # guess = knn_model.predict_proba(df)[0]
    # idx = np.argmax(guess)
    # if guess[idx] > .8:
    #     print(lbls[idx])
    # else:
    #     print("Unknown")
    # print(lbls)
    # print(guess)
    # print(np.argmax(guess))
    # print(knn_model.predict(df))
    # #print(knn_data['metadata'])