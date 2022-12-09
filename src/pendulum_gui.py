#! /usr/bin/env python3

# GUI object for pendulum simulation

# Project imports
import src.gui_widgets as gw

# Python imports

# 3rd-party imports
import numpy as np
import pygame

class PendulumGUI:
    """
    Graphic Interface used for playback of arm motions 
    """

    def __init__(self, double_pend=True, live=False):
        """
        Constructor of GUI sturcture

        Args:
            bool double_pend - use double pendulum model. if false, gui will 
                show a single pendulum arm instead
            bool live - set True if gui will be used for live playback
        """
        self.double_pend = double_pend
        self.live = live

        #Should gui die
        self._death = False

        pygame.init()
        # Build Scenery
        self.width = 800
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(pygame.Color('gray'))

        # Set up Font
        self.font = pygame.font.SysFont(None, 38)

        # Set Up Menu
        self.log_box = gw.Textbox(self.font, (20, 20))
        play_pos = (self.log_box.bottomleft[0], self.log_box.bottomleft[1] + 40)
        self.play = gw.Button(self.font, play_pos, 
            "Play", "dodgerblue1", "dodgerblue1")
        pause_pos = (self.play.topright[0] + 40, self.play.topright[1])
        self.pause = gw.Button(self.font, pause_pos, 
            "Pause", "firebrick3", "firebrick3")
        reset_pos = (self.pause.topright[0] + 40, self.pause.topright[1])
        self.reset = gw.Button(self.font, reset_pos, 
            "Reset", "forestgreen", "forestgreen")

        # If live disable buttons
        if self.live:
            self.play.deactivate()
            self.pause.deactivate()
            self.reset.deactivate()

        # Set up Status Panel
        self.state_box = gw.Textbox(self.font, (520, 150), "State: ")
        step_count_pos = (self.state_box.bottomleft[0], 
            self.state_box.bottomleft[1] + 30)
        self.step_count_box = gw.Textbox(self.font, step_count_pos, 
            "Step Count: ", "0")

        # Set up Pendulum
        self.pivot = gw.Ball((250, 225), 5, 'black')
        self.first_line = gw.Line(75, 'black', 26)
        self.first_ball = gw.Ball((250, 300), 12, 'red', 4, 'black')
        if self.double_pend:
            self.second_line = gw.Line(75, 'black', 26)
            self.second_ball = gw.Ball((250, 375), 12, 'red', 4, 'black')


    def draw(self):
        """
        Draw all widget in the gui
        """
        # Draw and update Gui
        self.screen.fill(pygame.Color('gray'))

        # Menu
        self.log_box.draw(self.screen)
        self.play.draw(self.screen)
        self.pause.draw(self.screen)
        self.reset.draw(self.screen)

        # Status Panel
        self.state_box.draw(self.screen)
        self.step_count_box.draw(self.screen)

        # Pendulum
        self.first_line.draw(self.screen, self.pivot.pos, self.first_ball.pos)
        self.pivot.draw(self.screen)
        if self.double_pend:
            self.second_line.draw(self.screen, self.first_ball.pos, 
                self.second_ball.pos)
            self.second_ball.draw(self.screen)
        self.first_ball.draw(self.screen)

        # Update canvas
        pygame.display.flip()


    def run_playback(self, logs_dict, fps=100):
        """
        Play the motions of the arm on the gui

        Args: 
            dict logs_dict - a dictionary contain the name of log file being
                plays, the target angles of the arm, and the state at the
                time
            int fps - maximum rate of the animation

        Note: This functions runs until gui is closed. Once the Gui is closed,
        the object should be discarded
        """
        # Make interal play state and clock
        playback_state = "Pause"
        clock = pygame.time.Clock()
        running = True
        idx = 0

        # Parse logs
        logfile_name = logs_dict['logname']
        log_states = logs_dict['logstates']
        theta1_array = logs_dict['theta1']
        steps_array = logs_dict['steps']
        if self.double_pend:
            theta2_array = logs_dict['theta2']
        
        max_idx = len(theta1_array)-1
        # Add logname
        self.log_box.dyn_text = f"Logfile: {logfile_name}"

        while running:
            #Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Button event handlers
                if self.play.pressed(event):
                    playback_state = "Play"
                elif self.pause.pressed(event):
                    playback_state = "Pause"
                elif self.reset.pressed(event):
                    playback_state = "Reset"

            # Get current metrics
            theta1 = theta1_array[idx]
            steps = steps_array[idx]
            class_state = log_states[idx]
            if self.double_pend:
                theta2 = theta2_array[idx]

            # Update class_state and step count
            self._update_status_panel(class_state, steps)

            # Update playback state, idx, and buttons
            idx, playback_state = self._update_buttons(idx, playback_state, 
                max_idx)

            # Update position of pendulum
            if self.double_pend:
                self._update_pendulum(theta1, theta2)
            else:
                self._update_pendulum(theta1)

            # Draw and update Gui
            self.draw()

            # Update
            clock.tick(fps)

        pygame.quit()


    def setup_live(self):
        """
        Set up gui for live playback
        """
        # Add logname
        self.log_box.dyn_text = f"Live!"

        # Draw and update Gui
        self.draw()
    

    def live_update(self, class_state, steps, theta1, theta2=None):
        """
        Update Gui widget from an external source

        Args:
            string class_state: current state to be displayed
            num steps: how many steps have been taken
            num theta1: angle of the first link (in radians)
            num theta2: if a double_pendulum simulation, angle of the second
                link (in radians). 
        """

        # Check for death
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._death = True

        # Update class_state and step count
        self._update_status_panel(class_state, steps)

        # Update position of pendulum
        if self.double_pend:
            self._update_pendulum(theta1, theta2)
        else:
            self._update_pendulum(theta1)

        # Draw and update Gui
        self.draw()

        return not self._death


    def await_death(self):
        """
        Disable gui and wait for user to close gui
        """
        if not self._death:
            # Add logname
            self.log_box.dyn_text = f"Session Over. Close Gui"

            running = True
            while running:
                #Check events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Draw and update Gui
                self.draw()
            
        pygame.quit()


    def _update_status_panel(self, class_state, steps):
        """
        Update the widgets showing the current state and step count

        Args:
            string class_state: current state 
            num steps: how many steps have been taken
        """
        self.state_box.dyn_text = class_state
        if class_state == "walking":
            self.state_box.update_dyn_color('blue')
        else:
            self.state_box.update_dyn_color('black')

        if class_state == "walking":
            self.step_count_box.dyn_text = str(steps)
        else:
            self.step_count_box.dyn_text = "N/a"

    def _update_buttons(self, idx, playback_state, max_idx):
        """
        Update whether the buttons should be pressable as well as
        the playback state and index along the playback

        Args:
            int idx - current index 
            string playback_state - current state of the playback; should be
                either "Play", "Pause", or "Reset" based on which button was 
                pressed
            int max_idx - maximum value idx can be
        """
        if playback_state == "Play":
            self.play.deactivate()
            self.pause.activate()
            self.reset.activate()
            if idx < max_idx:
                idx += 1
        
        elif playback_state == "Pause":
            self.pause.deactivate()
            self.play.activate()
            if idx == 0:
                self.reset.deactivate()
            else:
                self.reset.activate()
        
        elif playback_state == "Reset":
            playback_state = "Pause"
            self.pause.deactivate()
            self.reset.deactivate()
            self.play.activate()
            idx = 0

        return idx, playback_state

    def _update_pendulum(self, theta1, theta2=None):
        """
        Update the positions of the pendulum masses

        Args:
            num theta1 - angle of the first link (in radians)
            num theta2 - angle of the second link (in radians), set as None
                to indicate only a single-pendulum
        """
        new_fx = self.pivot.pos[0] + self.first_line.length*np.sin(theta1)
        new_fy = self.pivot.pos[1] + self.first_line.length*np.cos(theta1)
        self.first_ball.pos = (new_fx, new_fy)

        if theta2 is not None:
            new_sx = self.first_ball.pos[0] + \
                self.second_line.length*np.sin(theta1 + theta2)
            new_sy = self.first_ball.pos[1] + \
                self.second_line.length*np.cos(theta1 + theta2)
            self.second_ball.pos = (new_sx, new_sy)
