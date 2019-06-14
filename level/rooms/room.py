import pygame
from utilities.camera import Camera
from entities.geometry.rectangle import Rectangle


class Room(object):

    def __init__(self, building_id):
        self.bounds = None
        self.create_bounds()
        self.building_id = building_id
        self.exits = []
        self.make_exits()

    def create_bounds(self):
        # This method initializes the rectangle representing the dimensions of the room.
        raise NotImplementedError(
            "A class that inherits Room did not implement the create_bounds method")

    def make_exits(self):
        # This method initializes any rectangles representing exits to the room and adds
        # it to the exits list.
        raise NotImplementedError(
            "A class that inherits Room did not implement the make_exits method")

    def update(self, delta_time):
        raise NotImplementedError(
            "A class that inherits Room did not implement the update method")

    def draw(self, surface):
        # Temporary code, should draw sprites later
        self.bounds.draw(surface)
        for e in self.exits:
            e.draw(surface)
