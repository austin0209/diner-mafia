from pygame import Rect
from utilities.vector import Vector2
from utilities.camera import Camera


class Entity(object):
    def __init__(self, x=0, y=0, width=1, height=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bounds = Rect(self.x, self.y, self.width, self.height)
        self.location = Vector2(self.x, self.y)
        self.layer = 0

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.bounds = Rect(self.x, self.y, self.width, self.height)
        self.location = Vector2(self.x, self.y)

    def set_width(self, width):
        self.width = width
        self.bounds = Rect(self.x, self.y, self.width, self.height)

    def set_height(self, height):
        self.height = height
        self.bounds = Rect(self.x, self.y, self.width, self.height)

    def scaled_location(self):
        return Vector2(self.x * Camera.SCALE - Camera.TOP_LEFT.x, self.y * Camera.SCALE - Camera.TOP_LEFT.y)

    def scaled_width(self):
        return self.width * Camera.SCALE

    def scaled_height(self):
        return self.height * Camera.SCALE

    def update(self, delta_time):
        raise NotImplementedError(
            "A class that inherits Entity did not implement the update(delta_time) method")

    def draw(self, surface):
        raise NotImplementedError(
            "A class that inherits Entity did not implement the draw(surface) method")
