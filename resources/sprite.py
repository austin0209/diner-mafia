import pygame
import os
from enum import Enum
from entities.entity import Entity


class Type(Enum):
    NONE = 0
    PLAYER = 1
    NPC = 2
    BUBBLE = 3
    HOUSE_0 = 4


class Sprite(Entity):
    def __init__(self, x=0.0, y=0.0, sprite_type=Type.NONE):
        super(Sprite, self).__init__(x, y, 0, 0)
        self.type = sprite_type
        self.load_sprite()

    def sprite_setup(self, sprite_x=0, sprite_y=0, width=0, height=0, sprite_sheet_name=""):
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.set_width(width)
        self.set_height(height)
        self.sprite_sheet = pygame.image.load(
            'assets/sprites/{}'.format(sprite_sheet_name))

    def load_sprite(self):
        if self.type == Type.NONE:
            pass
        elif (self.type == Type.PLAYER):
            self.sprite_setup(2, 176, 11, 16, "sprites.png")
        elif (self.type == Type.NPC):
            self.sprite_setup(2, 176, 11, 16, "sprites.png")
        elif (self.type == Type.BUBBLE):
            self.sprite_setup(0, 192, 20, 20, "sprites.png")
        elif (self.type == Type.HOUSE_0):
            self.sprite_setup(0, 32, 48, 64, "sprites.png")

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.blit(self.sprite_sheet, (0, 0),
                        (self.sprite_x, self.sprite_y, self.width, self.height))

    def draw(self, surface):
        self.image = pygame.transform.scale(
            self.image, (int(self.scaled_width()), int(self.scaled_height())))
        surface.blit(self.image, (self.scaled_location().x,
                                  self.scaled_location().y))
