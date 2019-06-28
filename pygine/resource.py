import pygame
from enum import IntEnum
from pygine.base import PygineObject
from pygine.draw import draw_image
from pygine.utilities import Timer


class SpriteType(IntEnum):
    NONE = 0
    PLAYER_F = 1
    PLAYER_R = 2
    PLAYER_B = 3
    PLAYER_L = 4
    PLAYER_ARM_SIDE_F = 5
    PLAYER_ARM_SIDE_R = 6
    PLAYER_ARM_SIDE_B = 7
    PLAYER_ARM_SIDE_L = 8
    PLAYER_ARM_ABOVE_F = 9
    PLAYER_ARM_ABOVE_R = 10
    PLAYER_ARM_ABOVE_B = 11
    PLAYER_ARM_ABOVE_L = 12
    PLAYER_SHADOW = 13
    SIMPLE_HOUSE = 14
    SIMPLE_HOUSE_SHADOW = 15
    SPECIAL_HOUSE = 16
    SPECIAL_HOUSE_SHADOW = 17
    SHOP = 18
    SHOP_SHADOW = 19
    DINER = 20
    DINER_SHADOW = 21
    GRASS = 22
    TREE_THING = 23
    TREE_THING_SHADOW = 24
    SPEECH_BUBBLE = 25
    NPC_M_F = 26
    NPC_M_R = 27
    NPC_M_B = 28
    NPC_M_L = 29
    NPC_F_F = 30
    NPC_F_R = 31
    NPC_F_B = 32
    NPC_F_L = 33
    COFFEE_RAW = 34
    COFFEE_PRO = 35
    FISH_RAW = 36
    FISH_PRO = 37
    CROP_RAW = 38
    CROP_PRO = 39
    EGGS_RAW = 40
    EGGS_PRO = 41
    SIMPLE_HOUSE_INSIDE = 42
    SPECIAL_HOUSE_INSIDE = 43
    SHOP_INSIDE = 44
    DINER_INSIDE = 45
    FLOWER_POT = 46
    SOFA = 47
    BED = 48
    SHELF_EMPTY = 49
    SHELF_FULL = 50
    SHOP_COUNTER = 51
    STOOL_TALL = 52
    STOOL_SHORT = 53
    TABLE = 54
    PLATE = 55
    DINER_COUNTER = 56

    OCTOPUS = 57
    INK_BULLET = 58
    BOAT = 59
    WAVE = 60
    ROCK = 61

    SIDEWALK_LONG = 62
    SIDEWALK_TALL = 63
    TREE_CLUSTER = 64


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

    def set_frame(self, frame, columns):
        self.__sprite_x = self.__original_sprite_x + frame % columns * self.width
        self.__sprite_y = self.__original_sprite_y + \
                          int(frame / columns) * self.height
        self.__apply_changes_to_sprite()

    def increment_sprite_x(self, increment):
        self.__sprite_x += increment
        self.__apply_changes_to_sprite()

    def increment_sprite_y(self, increment):
        self.__sprite_y += increment
        self.__apply_changes_to_sprite()

    def _sprite_setup(self, sprite_x=0, sprite_y=0, width=0, height=0):
        self.__original_sprite_x = sprite_x
        self.__original_sprite_y = sprite_y
        self.__sprite_x = sprite_x
        self.__sprite_y = sprite_y
        self.set_width(width)
        self.set_height(height)

    def _load_sprite(self):
        if self.type == SpriteType.NONE:
            self._sprite_setup(1023, 1023, 1, 1)

        elif (self.type == SpriteType.PLAYER_F):
            self._sprite_setup(0, 624, 16, 32)
        elif (self.type == SpriteType.PLAYER_L):
            self._sprite_setup(0, 720, 16, 32)
        elif (self.type == SpriteType.PLAYER_B):
            self._sprite_setup(0, 688, 16, 32)
        elif (self.type == SpriteType.PLAYER_R):
            self._sprite_setup(0, 656, 16, 32)
        elif (self.type == SpriteType.PLAYER_ARM_SIDE_F):
            self._sprite_setup(96, 624, 16, 32)
        elif (self.type == SpriteType.PLAYER_ARM_SIDE_L):
            self._sprite_setup(96, 720, 16, 32)
        elif (self.type == SpriteType.PLAYER_ARM_SIDE_B):
            self._sprite_setup(96, 688, 16, 32)
        elif (self.type == SpriteType.PLAYER_ARM_SIDE_R):
            self._sprite_setup(96, 656, 16, 32)
        elif (self.type == SpriteType.PLAYER_ARM_ABOVE_F):
            self._sprite_setup(192, 624, 16, 32)
        elif (self.type == SpriteType.PLAYER_ARM_ABOVE_L):
            self._sprite_setup(192, 720, 16, 32)
        elif (self.type == SpriteType.PLAYER_ARM_ABOVE_B):
            self._sprite_setup(192, 688, 16, 32)
        elif (self.type == SpriteType.PLAYER_ARM_ABOVE_R):
            self._sprite_setup(192, 656, 16, 32)

        elif (self.type == SpriteType.PLAYER_SHADOW):
            self._sprite_setup(96, 752, 16, 32)

        elif (self.type == SpriteType.NPC_M_F):
            self._sprite_setup(0, 752, 16, 32)
        elif (self.type == SpriteType.NPC_M_L):
            self._sprite_setup(0, 784, 16, 32)
        elif (self.type == SpriteType.NPC_M_B):
            self._sprite_setup(0, 816, 16, 32)
        elif (self.type == SpriteType.NPC_M_R):
            self._sprite_setup(0, 848, 16, 32)

        elif (self.type == SpriteType.NPC_F_F):
            self._sprite_setup(0, 880, 16, 32)
        elif (self.type == SpriteType.NPC_F_L):
            self._sprite_setup(0, 912, 16, 32)
        elif (self.type == SpriteType.NPC_F_B):
            self._sprite_setup(0, 944, 16, 32)
        elif (self.type == SpriteType.NPC_F_R):
            self._sprite_setup(0, 976, 16, 32)

        elif (self.type == SpriteType.SPEECH_BUBBLE):
            self._sprite_setup(112, 752, 32, 32)

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
            self._sprite_setup(0, 592, 16, 16)
        elif (self.type == SpriteType.COFFEE_PRO):
            self._sprite_setup(0, 576, 16, 16)
        elif (self.type == SpriteType.FISH_RAW):
            self._sprite_setup(16, 592, 16, 16)
        elif (self.type == SpriteType.FISH_PRO):
            self._sprite_setup(16, 576, 16, 16)
        elif (self.type == SpriteType.CROP_RAW):
            self._sprite_setup(32, 592, 16, 16)
        elif (self.type == SpriteType.CROP_PRO):
            self._sprite_setup(32, 576, 16, 16)
        elif (self.type == SpriteType.EGGS_RAW):
            self._sprite_setup(48, 592, 16, 16)
        elif (self.type == SpriteType.EGGS_PRO):
            self._sprite_setup(48, 576, 16, 16)

        elif (self.type == SpriteType.SIMPLE_HOUSE_INSIDE):
            self._sprite_setup(0, 224, 160, 160)
        elif (self.type == SpriteType.SPECIAL_HOUSE_INSIDE):
            self._sprite_setup(160, 224, 288, 160)
        elif (self.type == SpriteType.SHOP_INSIDE):
            self._sprite_setup(448, 224, 288, 160)
        elif (self.type == SpriteType.DINER_INSIDE):
            self._sprite_setup(736, 224, 288, 160)

        elif (self.type == SpriteType.FLOWER_POT):
            self._sprite_setup(0, 416, 16, 48)
        elif (self.type == SpriteType.SOFA):
            self._sprite_setup(16, 432, 64, 32)
        elif (self.type == SpriteType.BED):
            self._sprite_setup(80, 400, 32, 64)
        elif (self.type == SpriteType.SHELF_EMPTY):
            self._sprite_setup(112, 400, 32, 64)
        elif (self.type == SpriteType.SHELF_FULL):
            self._sprite_setup(144, 400, 32, 64)
        elif (self.type == SpriteType.SHOP_COUNTER):
            self._sprite_setup(176, 416, 112, 48)
        elif (self.type == SpriteType.STOOL_TALL):
            self._sprite_setup(288, 432, 16, 32)
        elif (self.type == SpriteType.STOOL_SHORT):
            self._sprite_setup(304, 432, 16, 32)
        elif (self.type == SpriteType.TABLE):
            self._sprite_setup(320, 432, 32, 32)
        elif (self.type == SpriteType.SHELF_EMPTY):
            self._sprite_setup(352, 432, 32, 16)
        elif (self.type == SpriteType.DINER_COUNTER):
            self._sprite_setup(0, 480, 256, 80)

        elif (self.type == SpriteType.OCTOPUS):
            self._sprite_setup(112, 784, 16 * 3, 16 * 3)
        elif (self.type == SpriteType.INK_BULLET):
            self._sprite_setup(160, 800, 16, 16)
        elif (self.type == SpriteType.BOAT):
            self._sprite_setup(112, 880, 16 * 7, 16 * 5)
        elif (self.type == SpriteType.WAVE):
            self._sprite_setup(176, 880, 16, 16)
        elif (self.type == SpriteType.ROCK):
            self._sprite_setup(176, 784, 16 * 3, 16 * 2)

        elif (self.type == SpriteType.SIDEWALK_LONG):
            self._sprite_setup(32, 0, 608, 32)
        elif (self.type == SpriteType.SIDEWALK_TALL):
            self._sprite_setup(976, 592, 32, 272)            
        elif (self.type == SpriteType.TREE_CLUSTER):
            self._sprite_setup(368, 80, 64, 48)               

        self.__apply_changes_to_sprite()

    def __apply_changes_to_sprite(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.blit(SPRITE_SHEET, (0, 0),
                        (self.__sprite_x, self.__sprite_y, self.width, self.height))

    def draw(self, surface, camera_type):
        draw_image(surface, self.image, self.bounds, camera_type)


class Animation:
    def __init__(self, total_frames, columns, frame_duration):
        self.total_frames = total_frames
        self.columns = columns
        self.__frame_duration = frame_duration
        self.current_frame = 0
        self.__timer = Timer(self.__frame_duration)
        self.__timer.start()

    def update(self):
        self.__timer.update()
        if self.__timer.done:
            self.current_frame = self.current_frame + \
                                 1 if self.current_frame + 1 < self.total_frames else 0
            self.__timer.reset()
            self.__timer.start()
