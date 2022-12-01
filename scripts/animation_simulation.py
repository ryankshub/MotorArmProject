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
from utils import animate_simple_pend

# 3rd-party imports
import numpy as np

if __name__ == "__main__":
    # Display simple pendulum
    theta_trajs = np.array(np.linspace(0, np.pi/2, 50))
    animate_simple_pend(theta_trajs,L1=1,T=30)