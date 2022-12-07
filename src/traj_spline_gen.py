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

    def __init__(self, sample_rate, retract_angle = 0):
        """
        Constuctor for TrajSplineGenerator

        Args:
            num sample_rate - rate of incoming data
        """
        self._angle = 0
        self.time_till_step = -1
        self.sample_rate = sample_rate
        self._trajectory = deque()
        self._HOME_RATE = .001 # in rev/sample
        self.RETRACT_ANGLE = retract_angle
        self._DEGREE_THRES = .005 # in rev
    
    @property
    def angle(self):
        """
        Return current angle (in revolutions)
        """
        return self._angle

    @angle.setter
    def angle(self, value):
        """
        Update current_angle valye (in revolutions)

        Modify the angle to keep it in range (-.5, .5]
        """
        # Mod value to keep it between -0.5 and 0.5
        self._angle = value % 1
        if self._angle > .5:
            self._angle -= 1


    def get_degree_range(self, steps, time_window):
        """
        """
        if steps > 5:
            return -20/360
        else:
            return -30/360


    def generate_trajectory(self, target_angle, current_angle):
        """
        Generate bang-bang angle trajectory
        """
        # Get max velocity
        angle_disp = target_angle - current_angle
        max_vel = 2*angle_disp/self.time_till_step
        print(f"ANGLE_DIPS {angle_disp}, MAX_VEL {max_vel}")
        # Get the point where trajectory should hit maximum velocity
        # For this algorithm it's the half-way point
        half_samp = int(self.time_till_step*self.sample_rate*.5)
        half_vel_traj = np.linspace(0, max_vel, half_samp, endpoint=False)
        print(f"HALF_SAMP {half_samp}")
        # Combine velocities
        vel_traj = np.concatenate((half_vel_traj, 
                                   np.array([max_vel]),
                                   np.flip(half_vel_traj)))
        vel_traj = vel_traj/self.sample_rate
        print(f"VEL_TRAJ {vel_traj}, {sum(vel_traj)}")
        # Make trajectory
        angle_traj = []
        cand_angle = current_angle
        print(f"First CAND_ANGLE {cand_angle}")
        for vel in vel_traj:
            cand_angle += vel
            angle_traj.append(cand_angle)

        
        print(f"ANGLE_TRAJ {angle_traj}")
        return deque(angle_traj)

    
    def get_pos_setpoint(self, steps, time_window, time_till_step):
        """
        Calcuate the new position setpoint given the current
        number of steps in a time window

        Args:
            float steps - factional number of steps taken 
                (This is not an integer because it represents an average rate)
            float time_window - how long the steps rate was 
                measured over (in seconds)

        Rtn:
            The desired position angle(in revolutions) of the arm 
        """
        # Non walking behavior
        if steps == -1: 
            self._trajectory.clear() 
            if abs(self._angle) < self._DEGREE_THRES:
                return self._angle
            elif self._angle < 0.0:
                self.current_angle = (self._angle + self._HOME_RATE)
                return self._angle
            else:
                self.current_angle = (self._angle - self._HOME_RATE)
                return self._angle

        # walking behavior
        self.time_till_step = time_till_step
        if len(self._trajectory) == 0:
            # Get degree range
            degree_range = self.get_degree_range(steps, time_window)
            # Generate new trajectory
            if abs(degree_range - self._angle) < self._DEGREE_THRES:
                # Swing backward
                print("SWING BACK")
                self._trajectory = self.generate_trajectory(self.RETRACT_ANGLE,
                                                            self._angle)
            else:
                # Swing Forward
                print("SWING FORWARD")
                self._trajectory = self.generate_trajectory(degree_range, 
                                                            self._angle)
        return self._trajectory.popleft()
