import pygame
from utilities.color import Color
from utilities.camera import Camera
from entities.geometry.rectangle import Rectangle
from entities.world.building_type import BuildingType


class Room():

    def __init__(self, building_id, floor_num, total_floors, building_type=BuildingType.NORMAL, color=Color.GREEN):
        "When making a NORMAL or special building total floors should not exceed 1"
        self.color = color
        self.bounds = None
        self.create_bounds(building_type)
        self.building_id = building_id
        self.floor_num = floor_num
        self.exit = None
        self.stair_up = None
        self.stair_down = None
        self.make_stairs(floor_num, total_floors)

    def create_bounds(self, type):
        if type == BuildingType.NORMAL:
            self.bounds = Rectangle(0, 0, 6 * 16, 6 * 16, color=self.color)
        elif type == BuildingType.SPECIAL:
            self.bounds = Rectangle(0, 0, 12 * 16, 6 * 16, color=self.color)
        elif type == BuildingType.SHOP:
            self.bounds = Rectangle(0, 0, 18 * 16, 6 * 16, color=self.color)

    def make_stairs(self, floor_num, total_floors):
        if total_floors == 1:
            self.exit = Rectangle(self.bounds.x + self.bounds.width / 2 - 16,
                                  self.bounds.y + self.bounds.height - 16, 32, 16, color=Color.BLACK)
        else:
            if total_floors - 1 == floor_num:
                self.stair_down = Rectangle(32, 32, 32, 64, 0)
            elif floor_num == 0:
                self.stair_up = Rectangle(
                    self.bounds.width - 64, 32, 32, 64, 0)
                self.exit = Rectangle(
                    self.bounds.width / 2 - 16, self.bounds.height - 16, 32, 16, 0, Color.BLACK)
            else:
                self.stair_down = Rectangle(32, 32, 32, 64, 0)
                self.stair_up = Rectangle(
                    self.bounds.width - 64, 32, 32, 64, 0)

    def update(self, delta_time):
        pass

    def draw(self, surface):
        self.bounds.draw(surface)
        if self.exit != None:
            self.exit.draw(surface)
        if self.stair_up != None:
            self.stair_up.draw(surface)
        if self.stair_down != None:
            self.stair_down.draw(surface)
