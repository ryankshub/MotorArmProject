#! /usr/bin/env python3

# GUI environment for pendulum simulation

# Project imports

# Python imports

# 3rd-party imports
import pygame


## Class for ball objects
class Ball:
    """
    Ball objects for pendulum simulation
    """
    def __init__(self, pos, radius, inner_color='gray', width=0, 
        outer_color='black'):
        """
        Constructor for ball object in gui

        Args:
            tuple(int, int) pos - position of the ball (in pixels)
            int radius - raduis of the ball (in pixels)
            string or RGB tuple inner_color - color of the ball
            int width - thickness of the ball
            string or RGB tuple outer_color - color of the edge 
        """
        self.pos = pos
        self.radius = radius
        if (type(inner_color) == str):
            self.inner_color = pygame.Color(inner_color)
        else:
            self.inner_color = inner_color
        self.width = width
        if (type(outer_color) == str):
            self.outer_color = pygame.Color(outer_color)
        else:
            self.outer_color = outer_color

    def draw(self, bg):
        """
        Draws circle on canvas

        Args:
            pygame.surface bg - surface for the ball to be drawn on
        """
        # Draw circle
        pygame.draw.circle(bg, self.inner_color, self.pos, self.radius)
        # Draw edge
        if self.width > 0:
            pygame.draw.circle(bg, self.outer_color, self.pos, self.radius, 
                self.width)


## Class for Line object
class Line:
    """
    Line objects for pendulum simulation
    """
    def __init__(self, length, color='black', width=3):
        """
        Constuctor for the line object

        Args:
            int length (px) - how long the line should be
            string or RGB tuple color - color of the line
            int width - thickness of the line
        """
        self.length = length
        if (type(color) == str):
            self.color = pygame.Color(color)
        else:
            self.color = color
        self.width = width


    def draw(self, bg, start_pos, end_pos):
        """
        Draw line on background

        Args:
            pygame.surface bg - surface for the line to be drawn on
            tuple(int,int) start_pos - starting point of the line 
            tuple(int,int) end_pos - end point of the line
        """
        pygame.draw.line(bg, self.color, start_pos, end_pos)


class Textbox:
    """
    Textbox object for pendulum simulation
    """

    def __init__(self, font, pos, static_text="", dyn_text="", 
        dyn_color="black"):
        """
        Constructor for Textbox

        Args:
            pygame.font font - pygame font object for rendering text
            tuple(int,int) pos - position of the text box
            string static_text - Unchanging text of the textbox; precedes the
                dyn_text. 
            string dyn_text - dynamic text of th textbox; after the static text
            str or RGB tuple dyn_color - color of the dyntext
        """

        self.font = font
        self.pos = pos
        self.dyn_text = dyn_text
        self.update_dyn_color(dyn_color)

        # private because this should not change
        self._static_text = static_text 
        self._static_color = pygame.Color('black')


    def update_dyn_color(self, color):
        """
        Setter function for color

        Args:
            str or RGB tuple val - color of the dyntext
        """
        if (type(color) == str):
            self.dyn_color = pygame.Color(color)
        else:
            self.dyn_color = color


    def draw(self, bg):
        """
        Draw the textbox

        Args:
            pygame.surface bg - surface to be draw on
        """
        dyn_pose = self.pos

        if len(self._static_text) > 0:
            static_img = self.font.render(self._static_text, True, 
                self._static_color)
            dyn_pose = static_img.get_rect(topleft=self.pos).topright
            bg.blit(static_img, self.pos)
        
        if len(self.dyn_text) > 0:
            dyn_img = self.font.render(self.dyn_text, True, self.dyn_color)
            bg.blit(dyn_img, dyn_pose)

class Button:
    """
    Button class for pendumlum simulation
    """
    def __init__(self, font, pos, text="", font_color="black", 
        border_color="black", fade_color="gray36", press_color="gold1"):
        """
        Constructor for button class

        Args:
            pygame.font - font of button text
            tuple(int, int) - position of the button
            string text - Text inside button
            string or RGB tuple font_color - color of button's text
            string or RGB tuple border_color - color of button's border
            string or RGB tuple fade_color - color of button's text and border
                when button is inactive
            string or RGB tuple press_color - color of button's text and border
                when button is pressed
            int border_width - thickness of button's border
        """

        if(type(font_color) == str):
            self.font_color = pygame.Color(font_color)
        else:
            self.font_color = font_color

        if(type(border_color) == str):
            self.border_color = pygame.Color(border_color)
        else:
            self.border_color = border_color

        if(type(fade_color) == str):
            self.fade_color = pygame.Color(fade_color)
        else:
            self.fade_color = fade_color

        if(type(press_color) == str):
            self.press_color = pygame.Color(press_color)
        else:
            self.press_color = press_color

        self.font = font
        self.text = text
        self.button_img = font.render(text, True, font_color)
        button_pos = (pos[0] - 2, pos[1] - 2)
        self.button_rect = self.button_img.get_rect(topleft=button_pos)
        self.button_rect.width += 4
        self.button_rect.height += 4
        self.pos = pos
        self.border_width = 3
        self._active = True
        self._pressed = False

    def activate(self):
        """
        Make button pressable
        """
        self._active = True

    def deactivate(self):
        """
        Make button unpressable
        """
        self._active = False

    def pressed(self, event):
        """
        Event Handler for button

        Args: 
            pygame.event - pygame event taken place

        Return:
            True if button can execute event,
            False otherwise
        """
        # Check if button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN and self._active:
            if self.button_rect.collidepoint(event.pos):
                self._pressed = True
                return True

        if event.type == pygame.MOUSEBUTTONUP:
            self._pressed = False

        return False
    
    def draw(self, bg):
        """
        Draw button

        Args:
            pygame.surface bg - surface to be draw on
        """
        if self._pressed:
            self.button_img = self.font.render(self.text, True, 
                self.press_color)
            bg.blit(self.button_img, self.pos)
            pygame.draw.rect(bg, self.press_color, 
                self.button_rect, self.border_width)

        elif self._active:
            self.button_img = self.font.render(self.text, True, 
                self.font_color)
            bg.blit(self.button_img, self.pos)
            pygame.draw.rect(bg, self.border_color, 
                self.button_rect, self.border_width)

        else:
            self.button_img = self.font.render(self.text, True, 
                self.fade_color)
            bg.blit(self.button_img, self.pos)
            pygame.draw.rect(bg, self.fade_color, 
                self.button_rect, self.border_width)


if __name__ == "__main__":
    pygame.init()

    # Set up background
    screen = pygame.display.set_mode((960, 600))
    screen.fill(pygame.Color('gray'))
    
    # Font set up
    font = pygame.font.SysFont(None, 38)

    # Set up menu
    log_box = Textbox(font, (10, 10), "Logfile: SIM_test.txt")
    play = Button(font, (10, 70), "Play", "dodgerblue1", "dodgerblue1")
    pause_pos = (50, 70)#(play.button_rect.topright[0] + 20, 
        #play.button_rect.topright[1])
    pause = Button(font, pause_pos, "Pause", "firebrick3", "firebrick3")
    reset_pos = (100, 70)#(pause.button_rect.topright[0] + 20,
        #pause.button_rect.topright[1])
    reset = Button(font, reset_pos, "Reset", "forestgreen", "forestgreen")

    # Set up Status Panel
    state = Textbox(font, (740, 100), "State: ", "sitting")
    step_count = Textbox(font, (740, 150), "Step Count: ", "0")

    # Pendulum
    origin = Ball((360, 300), 5, 'black')
    first_ball = Ball((360, 375), 12, 'red', 2, 'black')
    second_ball = Ball((360, 450), 12, 'red', 2, 'black')
    first_line = Line(75, 'black', 7)
    second_line = Line(75, 'black', 7)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if play.pressed(event):
                print("Play")
            elif pause.pressed(event):
                print("Pause")
            elif reset.pressed(event):
                print("Reset")
            
        screen.fill(pygame.Color('gray'))
        # Lines
        first_line.draw(screen, origin.pos, first_ball.pos)
        second_line.draw(screen, first_ball.pos, second_ball.pos)
        # Ball
        origin.draw(screen)
        first_ball.draw(screen)
        second_ball.draw(screen)

        # Status Panel
        state.draw(screen)
        step_count.draw(screen)

        # Menu
        log_box.draw(screen)
        play.draw(screen)
        pause.draw(screen)
        reset.draw(screen)
        pygame.display.flip()
    pygame.quit()
    

