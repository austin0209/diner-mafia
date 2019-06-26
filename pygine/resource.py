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
    SHOP = 10
    SHOP_SHADOW = 11
    DINER = 12
    DINER_SHADOW = 13
    GRASS = 14
    TREE_THING = 15
    TREE_THING_SHADOW = 16
    SPEECH_BUBBLE = 17
    NPC_M_F = 18
    NPC_M_R = 19
    NPC_M_B = 20
    NPC_M_L = 21
    NPC_F_F = 22
    NPC_F_R = 23
    NPC_F_B = 24
    NPC_F_L = 25
    COFFEE_RAW = 26
    COFFEE_PRO = 27
    FISH_RAW = 28
    FISH_PRO = 29
    CROP_RAW = 30
    CROP_PRO = 31
    EGGS_RAW = 32
    EGGS_PRO = 33


SPRITE_SHEET = pygame.image.load(
    # '/home/cpi/games/Python/village-game/pygine/assets/sprites/sprites.png'
    'pygine/assets/sprites/sprites.png'
)


class Sprite(PygineObject):
    def __init__(self, x=0.0, y=0.0, sprite_type=SpriteType.NONE):
        super(Sprite, self).__init__(x, y, 0, 0)
        self.set_sprite(sprite_type)

    def set_sprite(self, sprite_type):
        self.type = sprite_type
        self._load_sprite()

    def _sprite_setup(self, sprite_x=0, sprite_y=0, width=0, height=0):
        self.__sprite_x = sprite_x
        self.__sprite_y = sprite_y
        self.set_width(width)
        self.set_height(height)

    def _load_sprite(self):
        if self.type == SpriteType.NONE:
            pass

        elif (self.type == SpriteType.PLAYER_F):
            self._sprite_setup(0, 288, 16, 32)
        elif (self.type == SpriteType.PLAYER_L):
            self._sprite_setup(0, 320, 16, 32)
        elif (self.type == SpriteType.PLAYER_B):
            self._sprite_setup(0, 352, 16, 32)
        elif (self.type == SpriteType.PLAYER_R):
            self._sprite_setup(0, 384, 16, 32)

        elif (self.type == SpriteType.PLAYER_SHADOW):
            self._sprite_setup(0, 240, 16, 32)

        elif (self.type == SpriteType.NPC_M_F):
            self._sprite_setup(112, 288, 16, 32)
        elif (self.type == SpriteType.NPC_M_L):
            self._sprite_setup(112, 320, 16, 32)
        elif (self.type == SpriteType.NPC_M_B):
            self._sprite_setup(112, 352, 16, 32)
        elif (self.type == SpriteType.NPC_M_R):
            self._sprite_setup(112, 384, 16, 32)

        elif (self.type == SpriteType.NPC_F_F):
            self._sprite_setup(224, 288, 16, 32)
        elif (self.type == SpriteType.NPC_F_L):
            self._sprite_setup(224, 320, 16, 32)
        elif (self.type == SpriteType.NPC_F_B):
            self._sprite_setup(224, 352, 16, 32)
        elif (self.type == SpriteType.NPC_F_R):
            self._sprite_setup(224, 384, 16, 32)

        elif (self.type == SpriteType.SPEECH_BUBBLE):
            self._sprite_setup(16, 240, 32, 32)

        elif (self.type == SpriteType.SIMPLE_HOUSE):
            self._sprite_setup(0, 64, 48, 64)
        elif (self.type == SpriteType.SIMPLE_HOUSE_SHADOW):
            self._sprite_setup(0, 128, 48, 64)
        elif (self.type == SpriteType.SPECIAL_HOUSE):
            self._sprite_setup(48, 64, 80, 64)
        elif (self.type == SpriteType.SPECIAL_HOUSE_SHADOW):
            self._sprite_setup(48, 128, 80, 64)
        elif (self.type == SpriteType.SHOP):
            self._sprite_setup(128, 32, 80, 96)
        elif (self.type == SpriteType.SHOP_SHADOW):
            self._sprite_setup(128, 128, 80, 96)
        elif (self.type == SpriteType.DINER):
            self._sprite_setup(208, 64, 128, 64)
        elif (self.type == SpriteType.DINER_SHADOW):
            self._sprite_setup(208, 128, 128, 64)

        elif (self.type == SpriteType.GRASS):
            self._sprite_setup(0, 0, 32, 32)
        elif (self.type == SpriteType.TREE_THING):
            self._sprite_setup(336, 96, 32, 32)
        elif (self.type == SpriteType.TREE_THING_SHADOW):
            self._sprite_setup(336, 128, 32, 32)

        elif (self.type == SpriteType.COFFEE_RAW):
            self._sprite_setup(0, 448, 16, 16)
        elif (self.type == SpriteType.COFFEE_PRO):
            self._sprite_setup(0, 432, 16, 16)
        elif (self.type == SpriteType.FISH_RAW):
            self._sprite_setup(16, 448, 16, 16)
        elif (self.type == SpriteType.FISH_PRO):
            self._sprite_setup(16, 432, 16, 16)
        elif (self.type == SpriteType.CROP_RAW):
            self._sprite_setup(32, 448, 16, 16)
        elif (self.type == SpriteType.CROP_PRO):
            self._sprite_setup(32, 432, 16, 16)
        elif (self.type == SpriteType.EGGS_RAW):
            self._sprite_setup(48, 448, 16, 16)
        elif (self.type == SpriteType.EGGS_PRO):
            self._sprite_setup(48, 432, 16, 16)

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.blit(SPRITE_SHEET, (0, 0),
                        (self.__sprite_x, self.__sprite_y, self.width, self.height))

    def draw(self, surface, camera_type):
        draw_image(surface, self.image, self.bounds, camera_type)
