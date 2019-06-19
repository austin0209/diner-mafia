import pygame
from enum import IntEnum
from pygine.base import PygineObject
from pygine.draw import draw_image


class SpriteType(IntEnum):
    NONE = 0
    PLAYER_F = 1
    PLAYER_R = 2
    PLAYER_B = 3
    PLAYER_L = 4
    PLAYER_SHADOW = 5
    SIMPLE_HOUSE = 6
    SIMPLE_HOUSE_SHADOW = 7
    SPECIAL_HOUSE = 8
    SPECIAL_HOUSE_SHADOW = 9
    GRASS = 10
    TREE_THING = 11
    TREE_THING_SHADOW = 12
    SPEECH_BUBBLE = 13
    NPC_M = 14
    NPC_F = 15


class Sprite(PygineObject):
    def __init__(self, x=0.0, y=0.0, sprite_type=SpriteType.NONE):
        super(Sprite, self).__init__(x, y, 0, 0)
        self.set_sprite(sprite_type)

    def set_sprite(self, sprite_type):
        self.type = sprite_type
        self.load_sprite()

    def sprite_setup(self, sprite_x=0, sprite_y=0, width=0, height=0, sprite_sheet_name=""):
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.set_width(width)
        self.set_height(height)
        self.sprite_sheet = pygame.image.load(
            # '/home/cpi/games/Python/village-game/pygine/assets/sprites/{}'.format(sprite_sheet_name)
            'pygine/assets/sprites/{}'.format(sprite_sheet_name)
        )

    def load_sprite(self):
        if self.type == SpriteType.NONE:
            pass
        elif (self.type == SpriteType.PLAYER_F):
            self.sprite_setup(0, 160, 16, 32, "sprites.png")
        elif (self.type == SpriteType.PLAYER_R):
            self.sprite_setup(16, 160, 16, 32, "sprites.png")
        elif (self.type == SpriteType.PLAYER_B):
            self.sprite_setup(32, 160, 16, 32, "sprites.png")
        elif (self.type == SpriteType.PLAYER_L):
            self.sprite_setup(48, 160, 16, 32, "sprites.png")
        elif (self.type == SpriteType.PLAYER_SHADOW):
            self.sprite_setup(64, 160, 16, 32, "sprites.png")

        elif (self.type == SpriteType.SIMPLE_HOUSE):
            self.sprite_setup(0, 32, 48, 64, "sprites.png")
        elif (self.type == SpriteType.SIMPLE_HOUSE_SHADOW):
            self.sprite_setup(0, 96, 48, 64, "sprites.png")
        elif (self.type == SpriteType.SPECIAL_HOUSE):
            self.sprite_setup(48, 32, 80, 64, "sprites.png")
        elif (self.type == SpriteType.SPECIAL_HOUSE_SHADOW):
            self.sprite_setup(48, 96, 80, 64, "sprites.png")

        elif (self.type == SpriteType.GRASS):
            self.sprite_setup(0, 0, 32, 32, "sprites.png")
        elif (self.type == SpriteType.TREE_THING):
            self.sprite_setup(128, 32, 32, 32, "sprites.png")
        elif (self.type == SpriteType.TREE_THING_SHADOW):
            self.sprite_setup(128, 64, 32, 32, "sprites.png")

        elif (self.type == SpriteType.SPEECH_BUBBLE):
            self.sprite_setup(0, 192, 22, 22, "sprites.png")
        elif (self.type == SpriteType.NPC_M):
            self.sprite_setup(80, 160, 16, 32, "sprites.png")
        elif (self.type == SpriteType.NPC_F):
            self.sprite_setup(96, 160, 16, 32, "sprites.png")

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.blit(self.sprite_sheet, (0, 0),
                        (self.sprite_x, self.sprite_y, self.width, self.height))

    def draw(self, surface, camera_type):
        draw_image(surface, self.image, self.bounds, camera_type)
