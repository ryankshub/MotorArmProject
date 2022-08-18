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
    def __init__(self, profiles, init_angle=0.0, EPSILON=0.01):
        """
        TrajectoryLookUp Constructor

        Args:
            dict(float -> filepath) profiles -
                A dictionary of speeds(in m/s) to filepaths containing the arm swing trajectories for
                those trajectories

            float init_angle - defaults to 0.0
                The initial angle of the arm(in rev). 0.0 points downward 

            float EPSILON - defaults to 10e-4
                precision to compare internal values
        """
        # Build profiles
        self._position_profiles = {}
        self._possible_speeds = []
        for speed_key in profiles:
            df = pd.read_csv(profiles[speed_key], names=["Position","Torque"])
            self._position_profiles[speed_key] = df["Position"]
            self._possible_speeds.append(speed_key)
        self._possible_speeds.sorted()

        # Parameters
        self._EPSILON = EPSILON
        self._time_normalizer = 30
        self._angle = init_angle
        self._past_angle = init_angle
        self._slow_idx = 0
        self._fast_idx = 0


    def _get_walk_speed(steps, time_window):
        """
        Convert step count from a certain window into an estimated walking speed

        TODO: The current model is based on data to fit RKS only
        """
        scaled_steps = steps *(self._time_normalizer/time_window)

        # Piecewise linear function model
        # These are derived from data
        if scaled_steps < 52:
            return (scaled_steps - 37)/15
        elif scaled_steps > 57:
            return (scaled_steps - 39)/15
        else:
            return (scaled_steps - 27)/25


    def _set_walk_speed(self, walk_speed):
        """
        """
        # If speed is too slow, bump it to slowest
        if walk_speed < self._possible_speeds[0]:
            return (None, self._possible_speeds[0])

        for i in range(1, len(self._possible_speeds)):
            cand_speed = self._possible_speeds[i]
            # If speed is equal to cand speed
            if (abs(walk_speed - cand_speed) < self._EPSILON):
                return (None, cand_speed)
            
            # If speed if less than cand speed
            elif walk_speed < cand_speed:
                return (self._possible_speeds[i-1], cand_speed)

        # If speed is too fast, cap it to fastest 
        return (None, self._possible_speeds[-1])

    def _search_trajs(walk_speed):
        """
        """
        for speed in self._possible_speeds:



    def _blend_traj(slow_speed, fast_speed, curr_speed):
        alpha = (fast_speed - curr_speed)/(fast_speed - slow_speed)
        slow_value = self._position_profiles[slow_speed][self._slow_idx]
        fast_value = self._position_profiles[fast_speed][self._fast_idx]
        return alpha*slow_value + (1-alpha)*fast_value
    

    def get_pos_setpoint(steps, time_window, time_stamp):
        pass


    def get_angle(self, angle):
        self._past_angle = self._angle
        self._angle = angle
