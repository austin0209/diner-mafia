import pygame
import random
from utilities.color import Color
from utilities.camera import Camera
from utilities.vector import Vector2
from entities.entity import Entity
from entities.geometry.rectangle import Rectangle
from resources.sprite import Sprite
from resources.sprite import Type


class Npc(Entity):

    PROXIMITY = 25

    def __init__(self, x, y):
        super(Npc, self).__init__(x, y, 11, 16)
        self.rect = Rectangle(x, y, self.width, self.height)
        self.pref = random.randint(0, 3)
        self.select_pref()
        self.talking = False
        self.sprite = Sprite(x, y, Type.NPC)
        self.speech_bubble = Sprite(x + 6, y - 17, Type.BUBBLE)

    def select_pref(self):
        if self.pref == 0:
            self.color = Color.RED
        elif self.pref == 1:
            self.color = Color.BLUE
        elif self.pref == 2:
            self.color = Color.GREEN
        elif self.pref == 3:
            self.color = Color.WHITE

    def set_location(self, x, y):
        super(Npc, self).set_location(x, y)
        self.rect.set_location(self.x, self.y)
        self.sprite.set_location(self.x, self.y)
        self.speech_bubble.set_location(self.x + 6, self.y - 17)

    def center(self):
        return Vector2(self.x + self.width / 2, self.y + self.height / 2)

    def update(self, game_time):
        pass

    def draw(self, surface):
        self.sprite.draw(surface)
        if (self.talking):
            self.speech_bubble.draw(surface)
