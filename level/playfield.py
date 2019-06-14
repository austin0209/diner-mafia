from entities.user.player import Player
from entities.npcs.npc import Npc
from entities.world.building import Building
from entities.world.building_type import BuildingType
from entities.world.resourcehub import ResourceHub
from utilities.vector import Vector2
from utilities.color import Color
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera
# TEMP IMPORT
import random


class Playfield:
    ENTITIES = []
    BUILDINGS = []
    OUTSIDE = True
    CURRENT_ROOM = None

    def __init__(self):
        self.camera = Camera()
        self.camera_location = Vector2(0, 0)
        self.input = Input()
        self.player = None
        self.reset()

    def reset(self):
        Playfield.ENTITIES = []
        Playfield.ENTITIES.append(Npc(150, 90))
        for i in range(10):
            Playfield.ENTITIES.append(Npc(random.randint(
                0, Camera.BOUNDS.width), random.randint(0, Camera.BOUNDS.height)))
        Playfield.ENTITIES.append(ResourceHub(30, 30, 30, 30, 1))
        Playfield.BUILDINGS.append(
            Building(200, Camera.BOUNDS.height / 2 - 100, len(Playfield.BUILDINGS), BuildingType.SPECIAL))
        for b in Playfield.BUILDINGS:
            Playfield.ENTITIES.append(b)
        self.player = Player(10, 10, 11, 16)
        Playfield.ENTITIES.append(self.player)

    def update_camera(self):
        center = Vector2(self.player.x - Camera.BOUNDS.width / 2 + self.player.width / 2,
                         self.player.y - Camera.BOUNDS.height / 2 + self.player.height / 2)
        self.camera.update(center)

    def update_input(self):
        self.input.update()

    def y_key(self, entity):
        return entity.y + entity.height

    def update_entities(self, delta_time):
        if Playfield.OUTSIDE:
            for i in range(len(Playfield.ENTITIES) - 1, -1, -1):
                Playfield.ENTITIES[i].update(delta_time)
        else:
            self.player.update(delta_time)
        Playfield.ENTITIES.sort(key=self.y_key)

    def update(self, delta_time):
        self.update_camera()
        self.update_input()
        self.update_entities(delta_time)
        if not Playfield.OUTSIDE:
            Playfield.CURRENT_ROOM.update(delta_time)

    def draw(self, surface):
        if Playfield.OUTSIDE:
            for i in range(len(Playfield.ENTITIES)):
                Playfield.ENTITIES[i].draw(surface)
        else:
            Playfield.CURRENT_ROOM.draw(surface)
            self.player.draw(surface)
