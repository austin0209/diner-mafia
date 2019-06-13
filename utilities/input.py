import pygame
from enum import Enum


class InputType(Enum):
    NONE = 0

    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    A = 5
    B = 6
    X = 7
    Y = 8
    START = 9
    SELECT = 10    

    RESET = 11
    TOGGLE_FULLSCREEN = 12
    QUIT = 13


class Input:
    def __init__(self):
        self.key_state = None

    def pressing(self, type=InputType.NONE):
        if type == InputType.UP:
            return self.key_state[pygame.K_UP] or self.key_state[pygame.K_w]
        if type == InputType.LEFT:
            return self.key_state[pygame.K_LEFT] or self.key_state[pygame.K_a]
        if type == InputType.DOWN:
            return self.key_state[pygame.K_DOWN] or self.key_state[pygame.K_s]
        if type == InputType.RIGHT:
            return self.key_state[pygame.K_RIGHT] or self.key_state[pygame.K_d]
        if type == InputType.A:
            return self.key_state[pygame.K_j]
        if type == InputType.B:
            return self.key_state[pygame.K_k]
        if type == InputType.X:
            return self.key_state[pygame.K_u]
        if type == InputType.Y:
            return self.key_state[pygame.K_i]
        if type == InputType.SELECT:
            return self.key_state[pygame.K_SPACE]
        if type == InputType.START:
            return self.key_state[pygame.K_KP_ENTER]

        if type == InputType.RESET:
            return self.key_state[pygame.K_r]
        if type == InputType.TOGGLE_FULLSCREEN:
            return self.key_state[pygame.K_F10]
        if type == InputType.QUIT:
            return self.key_state[pygame.K_ESCAPE] or self.key_state[pygame.K_BACKSPACE]
            
        return False

    def update(self):
        self.key_state = pygame.key.get_pressed()
