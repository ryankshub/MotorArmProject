#! /usr/bin/env python3
"""
File for Trajectory Look-up Class
"""

# Project Import

# Python Import
import pandas as pd
# 3rd-Party Import

class TrajectoryLookUp():
    """
    A look-up table to determine the position set-point by referencing gait profiles of
    different speed
    """
    def __init__(self, profiles, step_speed_model=None, EPSILON=10e-4):
        """
        TrajectoryLookUp Constructor

        TODO
        """
        pass

    def _get_walk_speed(steps, time_window):
        pass

    def _search_trajs(walk_speed):
        pass

    def _blend_traj(slow_traj, fast_traj, time_stamp):
        pass
    
    def get_position(steps, time_window, time_stamp):
        pass
