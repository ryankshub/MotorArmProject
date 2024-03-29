#! /usr/bin/env python3

# Spline generator for angle trajectory

# Python imports
from collections import deque

# Project imports

# 3rd-party imports
import numpy as np


class TrajectorySplineGenerator:
    """
    Generates a bang-bang angle trajectory 
    """

    def __init__(self, sample_rate, double_pend = False):
        """
        Constuctor for TrajSplineGenerator

        Args:
            num sample_rate - rate of incoming data
            bool double_pend - set True to return should angles as well
        """
        # Set public members
        self.time_till_step = -1
        self.sample_rate = sample_rate

        # Set private members
        self._elbow_angle = 0
        if double_pend:
            self._shoulder_angle = 0
        else:
            self._shoulder_angle = None
        self._double_pend = double_pend
        self._el_trajectory = deque()
        self._sh_trajectory = deque()
        self._time_normalizer = 30
        self._HOME_RATE = .001 # in rev/sample
        self._DEGREE_THRES = .005 # in rev
        self._MIN_TIME_NEEDED = 0.2 
        self._swing_forward = True

        # NOTE: The following constants are based on information from:
        # Perry J, Burnfield JM.
        # Gait Analysis: Normal and Pathological Function
        # Second Edition (pp 131 - 136)
        # We used two measurements from the above to construct a linear 
        # projection for shoulder extension and elbow flexion for other speeds
        # constant for getting shoulder range
        self._SHOULDER_MAX_FLEX = -8/360 # Max shoulder flex in revolutions
        self._SHOULDER_BASE_ANGLE = 24 # Baseline angle in degs
        self._SHOULDER_BASE_SPEED = 92/60 # baseline speed for look-up table
        self._SHOULDER_ANGLE_CONV = .6/7 # speed_diff/angle_diff 

        # constants for getting elbow range
        self._ELBOW_MAX_EXT = -17/360 # Max elbow extension in revolutions
        self._ELBOW_BASE_ANGLE = -47 # Baseline angle in degs
        self._ELBOW_BASE_SPEED = 92/60 #baseline speed for look-up table
        self._ELBOW_ANGLE_CONV = .6/8 # speed_diff/angle_diff
    
    @property
    def angle(self):
        """
        Return current angle (in revolutions)
        """
        return self._elbow_angle

    @angle.setter
    def angle(self, value):
        """
        Update current_angle value (in revolutions)

        Modify the angle to keep it in range (-.5, .5]
        """
        # Mod value to keep it between -0.5 and 0.5
        self._elbow_angle = value % 1
        if self._elbow_angle > .5:
            self._elbow_angle -= 1

    @property
    def sh_angle(self):
        """
        Return current shoulder angle (in revolutions)
        NOTE: only update if double pendulum is true
        """
        return self._shoulder_angle

    @sh_angle.setter
    def sh_angle(self, value):
        """
        Update current shoulder angle value (in revolutions)

        Modify the angle to keep it in range (-.5, .5]
        """
        if self._double_pend:
            self._shoulder_angle = value % 1
            if self._shoulder_angle > .5:
                self._shoulder_angle -= 1


    # TrajectorySplineGenertor private fcns
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


    def _get_pos_double_pendulum(self, steps, time_window, time_till_step):
        """
        Calculates return angle for the elbow angle and shoulder angle

        Args:
            float steps - factional number of steps taken 
                (This is not an integer because it represents an average rate)
            float time_window - how long the steps rate was 
                measured over (in seconds)
            float time_till_step - estimated number of seconds until the next
                step
        Rtn:
            Tuple of the desired (elbow, shoulder) angles
        """
        # Non walking behavior
        if steps == -1: 
            self._el_trajectory.clear()
            self._sh_trajectory.clear()

            # Update Elbow
            if abs(self._elbow_angle) < self._DEGREE_THRES:
                pass
            elif self._elbow_angle < 0.0:
                self.angle = (self._elbow_angle + self._HOME_RATE)
            else:
                self.angle = (self._elbow_angle - self._HOME_RATE)

            # Update Shoulder
            if abs(self._shoulder_angle) < self._DEGREE_THRES:
                pass
            elif self._shoulder_angle < 0.0:
                self.sh_angle = (self._shoulder_angle + self._HOME_RATE)
            else:
                self.sh_angle = (self._shoulder_angle - self._HOME_RATE)

            # return new desired angles
            return self._elbow_angle, self._shoulder_angle

        else:
            # walking behavior
            self.time_till_step = time_till_step
            if len(self._el_trajectory) == 0:

                # If we are looking for a step, wait for a bit
                if self.time_till_step <= self._MIN_TIME_NEEDED:
                    return self._elbow_angle, self._shoulder_angle

                # Elbow flex and shoulder_ext angle
                est_speed = self._conv_step_speed(steps, time_window)
                elbow_flex = self.get_elbow_flex_angle(est_speed)
                shoulder_ext = self.get_shoulder_ext_angle(est_speed)

                # Generate new trajectory
                if self._swing_forward:
                    # Swing Forward
                    self._el_trajectory = \
                        self.generate_trajectory(elbow_flex, 
                                                 self._elbow_angle)
                    self._sh_trajectory = \
                        self.generate_trajectory(self._SHOULDER_MAX_FLEX,
                                                 self._shoulder_angle)
                    self._swing_forward = False

                else:
                    # Swing backward
                    self._el_trajectory = \
                        self.generate_trajectory(self._ELBOW_MAX_EXT,
                                                 self._elbow_angle)
                    self._sh_trajectory = \
                        self.generate_trajectory(shoulder_ext,
                                                 self._shoulder_angle)
                    self._swing_forward = True

            return self._el_trajectory.popleft(), self._sh_trajectory.popleft()
    

    def _get_pos_single_pendulum(self, steps, time_window, time_till_step):
        """
        Calculates return angle for just the elbow angle

        Args:
            float steps - factional number of steps taken 
                (This is not an integer because it represents an average rate)
            float time_window - how long the steps rate was 
                measured over (in seconds)
            float time_till_step - estimated number of seconds until the next
                step
        
        Rtn:
            tuple of desired elbow_angle, None
        """
        # Non walking behavior
        if steps == -1: 
            self._el_trajectory.clear() 
            if abs(self._elbow_angle) < self._DEGREE_THRES:
                return self._elbow_angle, None
            elif self._elbow_angle < 0.0:
                self.angle = (self._elbow_angle + self._HOME_RATE)
                return self._elbow_angle, None
            else:
                self.angle = (self._elbow_angle - self._HOME_RATE)
                return self._elbow_angle, None

        # walking behavior
        self.time_till_step = time_till_step
        if len(self._el_trajectory) == 0:

            # If we are looking for a step, wait for a bit
            if self.time_till_step <= self._MIN_TIME_NEEDED:
                return self._elbow_angle, None
 
            # Elbow flex angle
            est_speed = self._conv_step_speed(steps, time_window)
            elbow_flex = self.get_elbow_flex_angle(est_speed)

            # Generate new trajectory
            if self._swing_forward:
                # Swing Forward
                self._el_trajectory = \
                    self.generate_trajectory(elbow_flex, 
                                             self._elbow_angle)
                self._swing_forward = False
 
            else:
                # Swing backward
                self._el_trajectory = \
                    self.generate_trajectory(self._ELBOW_MAX_EXT,
                                             self._elbow_angle)
                self._swing_forward = True

        return self._el_trajectory.popleft(), None


    # TrajSplineGenerator public fcn
    def generate_trajectory(self, target_angle, current_angle):
        """
        Generate bang-bang angle trajectory

        Args:
            num target_angle - desired end angle of trajectory (in revolutions)
            num current_angle - desired start angle of trajectory 
                (in revolutions)
        """
        # Get max velocity
        angle_disp = target_angle - current_angle
        max_vel = 2*angle_disp/self.time_till_step
        
        # Get the point where trajectory should hit maximum velocity
        # For this algorithm it's the half-way point
        half_samp = int(self.time_till_step*self.sample_rate*.5)
        half_vel_traj = np.linspace(0, max_vel, half_samp, endpoint=False)

        # Combine velocities
        vel_traj = np.concatenate((half_vel_traj, 
                                   np.array([max_vel]),
                                   np.flip(half_vel_traj)))
        vel_traj = vel_traj/self.sample_rate

        # Make trajectory
        angle_traj = []
        cand_angle = current_angle

        for vel in vel_traj:
            cand_angle += vel
            angle_traj.append(cand_angle)

        return deque(angle_traj)


    def get_elbow_flex_angle(self, est_speed):
        """
        Calculate the elbow flex angle based on estimated walk speed and numbers
        from Gait Analysis: Normal and Pathological Function

        Args:
            num est_speed - estimated walk speed (in m/s)
        Rtn:
            num elbow flex angle in revolutions
        """
        # Get Elbow flex angle
        angle_diff = \
            (self._ELBOW_BASE_SPEED - est_speed)/self._ELBOW_ANGLE_CONV
        angle_deg = self._ELBOW_BASE_ANGLE + angle_diff
        return angle_deg/360


    def get_shoulder_ext_angle(self, est_speed):
        """
        Calculate the shoulder extension angle based on estimated walk speed and
        number from Gait Analysis: Normal and Pathological Function

        Args:
            num est_speed - estimated walk speed (in m/s)
        Rtn:
            num shoulder extension angle in revolutions
        """
        # Get shoulder ext angle
        angle_diff = \
            (self._SHOULDER_BASE_SPEED - est_speed)/self._SHOULDER_ANGLE_CONV
        angle_deg = self._SHOULDER_BASE_ANGLE - angle_diff
        return angle_deg/360

    
    def get_pos_setpoint(self, steps, time_window, time_till_step):
        """
        Calcuate the new position setpoint given the current
        number of steps in a time window

        Args:
            float steps - factional number of steps taken 
                (This is not an integer because it represents an average rate)
            float time_window - how long the steps rate was 
                measured over (in seconds)
            float time_till_step - estimated number of seconds until the next
                step
    def get_elbow_flex_angle(self, est_speed):
        """
        """
        # Get Elbow flex angle
        angle_diff = \
            (self._ELBOW_BASE_SPEED - est_speed)/self._ELBOW_ANGLE_CONV
        angle_deg = self._ELBOW_BASE_ANGLE + angle_diff
        return angle_deg/360
        Rtn:
            tuple of desired position angles(in revolutions) of the arm in the
                order (elbow, shoulder)
            If the function is using a single pendulum model, the shoulder angle
                will be set to None 
        """
        if self._double_pend:
            return self._get_pos_double_pendulum(steps, 
                                                 time_window, 
                                                 time_till_step)
        else:
            return self._get_pos_single_pendulum(steps,
                                                 time_window,
                                                 time_till_step)



    

    
    
