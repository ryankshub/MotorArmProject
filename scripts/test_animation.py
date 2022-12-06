#! /usr/bin/env python3

# Testing script for animations

# Python imports
import os
import sys

# Add Project root for imports
FILE_PATH = sys.path[0]
ROOT_PATH = os.path.join(FILE_PATH, '..')
sys.path.append(ROOT_PATH)

# Project import
from src import PendulumGUI

# 3rd-party imports
import numpy as np

if __name__ == "__main__":
    # Display simple pendulum
    first_angles = np.arange(0, np.pi/2, np.pi/180)
    second_angles = np.arange(-np.pi/4, np.pi/4, np.pi/180)

    first_angles = np.concatenate((first_angles, np.flip(first_angles)))
    second_angles = np.concatenate((second_angles, np.flip(second_angles)))

    second_angles = second_angles[:len(first_angles)]

    logstates = ["rising"]*(len(second_angles)//2) + \
        ["walking"]*(len(second_angles)//2)
    steps = [i for i in range(len(second_angles))]

    app = PendulumGUI()
    app.run_playback({"logname": "SIM_testing.txt",
                      "logstates": logstates,
                      "theta1": first_angles,
                      "theta2": second_angles,
                      "steps": steps})