# TODO: Add the following: ButtonTrigger, TimedTrigger
from enum import IntEnum

class Direction(Enum):
    NONE = 0,
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4

class Trigger(object):
    def __init__(self, next_scene):
        self.next = int(next_scene)
    
    def update(self):
        raise NotImplementedError(
            "A class that inherits Trigger did not implement the update(surface) method")

    def draw(self):
        raise NotImplementedError(
            "A class that inherits Trigger did not implement the draw(surface) method")


class CollisionTrigger(Trigger):
    def __init__(self, next_scene, x, y, width, height, direction=UP):
        super(CollisionTrigger, self).__init__(next_scene)
