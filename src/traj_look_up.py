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
    A look-up table to determine the position set-point by referencing gait 
    profiles of different speed
    """
    def __init__(self, profiles, init_angle=0.0, EPSILON=0.01):
        """
        TrajectoryLookUp Constructor

        Args:
            dict(float -> filepath) profiles -
                A dictionary of speeds(in m/s) to filepaths containing the arm 
                swing trajectories for those trajectories

            float init_angle - defaults to 0.0
                The initial angle of the arm(in rev). 0.0 points downward 

            float EPSILON - defaults to 0.01
                precision to compare internal values
        """
        # Build profiles
        self._position_profiles = {}
        self._possible_speeds = []
        for speed_key in profiles:
            df = pd.read_csv(profiles[speed_key], names=["Position","Torque"])
            self._position_profiles[speed_key] = df["Position"]
            self._possible_speeds.append(speed_key)
        self._possible_speeds.sort()

        # Parameters
        self._EPSILON = EPSILON
        self._HOME_RATE = 0.001
        self._time_normalizer = 30
        self._angle = init_angle
        self._past_angle = init_angle
        self._curr_speed = 0.0

        self._slow_speed = 0.0
        self._slow_index = 0
        self._slow_incre = 0

        self._fast_speed = 0.0
        self._fast_index = 0
        self._fast_incre = 0


    # TrajLookUp properties
    @property
    def angle(self):
        """
        Return current value of elbow angle in revolutions
        """
        return self._angle


    @angle.setter
    def angle(self, value):
        """
        Update elbow angle and past elbow angle

        Args:
            num value - new elbow angle (in revolutions)
        """
        self._past_angle = self._angle
        # Mod value to keep it between -0.5 and 0.5
        self._angle = value % 1
        if self._angle > .5:
            self._angle -= 1

    @property
    def sh_angle(self):
        """
        This property is added for consistency across trajectory generating 
        objects. TrajLookUp does not support a shoulder angle, always return 
        None
        """
        return None

    @sh_angle.setter
    def sh_angle(self, value):
        """
        This property is added for consistency across trajectory generating
        objects. TrajLookUp does not support a shoulder angle, always ignore
        new value
        """
        pass

    
    # TrajLookUp private fcns
    def _blend_traj(self, slow_speed, fast_speed, curr_speed,
         slow_idx, fast_idx):
        """
        Blend two trajectory position set points into one

        Args:
            slow_speed: slower of the two trajectories
            fast_speed: faster of the two trajectories
            curr_speed: current walking speed
            slow_idx: current idx of the slow traj
            fast_idx: current idx of the fast traj

        Rtn:
            blended trajectory positions
        """
        alpha = (fast_speed - curr_speed)/(fast_speed - slow_speed)
        slow_value = self._position_profiles[slow_speed][slow_idx]
        fast_value = self._position_profiles[fast_speed][fast_idx]
        return alpha*slow_value + (1-alpha)*fast_value


    def _conv_step_speed(self, steps, time_window):
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


    def _get_walk_speeds(self, curr_speed):
        """
        Determine which pre-set walking speeds are closest to 
        the current walking speed

        Args:
            float curr_speed: estimated walk speed

        Rtn:
            A tuple of (slow_speed, fast_speed) where
                slow_speed < curr_speed and fast_speed > curr_speed
            If curr_speed is already a pre-set walking speed, the
            slow_speed will be None
        """
        # If speed is too slow, bump it to slowest
        if curr_speed < self._possible_speeds[0]:
            return (None, self._possible_speeds[0])

        for i in range(1, len(self._possible_speeds)):
            cand_speed = self._possible_speeds[i]
            # If speed is equal to cand speed
            if (abs(curr_speed - cand_speed) < self._EPSILON):
                return (None, cand_speed)
            
            # If speed if less than cand speed
            elif curr_speed < cand_speed:
                return (self._possible_speeds[i-1], cand_speed)

        # If speed is too fast, cap it to fastest 
        return (None, self._possible_speeds[-1])


    def _search_trajs(self, preset_speed):
        """
        Search for where along the trajectory the
        arm currently is

        Args:
            float preset_speed : 
                Preset speed in the profiles
        
        Rtn:
            tuple(int,int) 
                -index of where arm is in trajectory
                -amount to increment look-up
        """
        # Get swing condition
        # True = Swing Forward, False = Swing Backward
        swing_cond = (self._angle <= self._past_angle)
        pos_df = self._position_profiles[preset_speed]
        diff_df = abs(pos_df - self._angle)

        length = len(pos_df)
        min_idx = diff_df.idxmin()
        if (pos_df[min_idx] <= pos_df[(min_idx-1) % length]) == swing_cond:
            return (min_idx, 1)
        else:
            return (min_idx, -1)


    # TrajLookUp public fcns
    def get_pos_setpoint(self, steps, time_window, time_till_step=None):
        """
        Calcuate the new position setpoint given the current
        number of steps in a time window

        Args:
            float steps - factional number of steps taken 
                (This is not an integer because it represents an average rate)
            float time_window - how long the steps rate was measured over 
                (in seconds)

        Rtn:
            The desired position angle(in revolutions) of the arm 
        """
        # Check if walking
        if steps == -1:  
            if abs(self._angle) < .001:
                return self._angle, None
            elif self._angle < 0.0:
                self.angle = (self._angle + self._HOME_RATE)
                return self._angle, None
            else:
                self.angle = (self._angle - self._HOME_RATE)
                return self._angle, None

        # Get new speed
        est_speed = self._conv_step_speed(steps, time_window)

        # Check if change is drastic enough to alter trajectories
        if (abs(self._curr_speed - est_speed) > 3*self._EPSILON):
            # Calculate new slow/fast speed
            self._curr_speed = est_speed
            self._slow_speed, self._fast_speed = \
                self._get_walk_speeds(self._curr_speed)
            self._fast_index, self._fast_incre = \
                self._search_trajs(self._fast_speed)

            if self._slow_speed:
                self._slow_index, self._slow_incre = \
                    self._search_trajs(self._slow_speed)
            else:
                self._slow_index = None

        # Calculate return set_point
        rtn_setpoint = 0.0
        if self._slow_speed:
            #Update index
            self._slow_index = (self._slow_index + self._slow_incre) % \
                len(self._position_profiles[self._slow_speed])
            self._fast_index = (self._fast_index + self._fast_incre) % \
                len(self._position_profiles[self._fast_speed])
                
            #Update setpoint
            rtn_setpoint = self._blend_traj(self._slow_speed, 
                                            self._fast_speed, 
                                            self._curr_speed,
                                            self._slow_index, 
                                            self._fast_index)

        else:
            #Update index
            self._fast_index = (self._fast_index + self._fast_incre) % \
                len(self._position_profiles[self._fast_speed])
            #Update setpoint
            rtn_setpoint = \
                self._position_profiles[self._fast_speed][self._fast_index]

        return rtn_setpoint, None