from entities.user.player import Player
from entities.world.building import Building
from utilities.vector import Vector2
from utilities.color import Color
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera


class Playfield:
    ENTITIES = []
    BUILDINGS = []
    OUTSIDE = True
    CURRENT_ROOM = None

    def __init__(self):
        self.camera = Camera()
        self.camera_location = Vector2(0, 0)
        self.input = Input()
        self.reset()

    def reset(self):
        Playfield.ENTITIES = []
        Playfield.ENTITIES.append(Player(10, 10, 10, 10))
        Playfield.BUILDINGS.append(Building(10, Camera.BOUNDS.height / 2 - 100, 3, len(Playfield.BUILDINGS)))
        Playfield.BUILDINGS.append(Building(200, Camera.BOUNDS.height / 2 - 100, 1, len(Playfield.BUILDINGS)))
        for b in Playfield.BUILDINGS:
            Playfield.ENTITIES.append(b)

    def update_camera(self):
        self.camera.update()

    def update_input(self):
        self.input.update()

    def update_entities(self, delta_time):
        if Playfield.OUTSIDE:
            for i in range(len(Playfield.ENTITIES) - 1, -1, -1):
                Playfield.ENTITIES[i].update(delta_time)
        else:
            Playfield.ENTITIES[0].update(delta_time)

    def update(self, delta_time):
        self.update_camera()
        self.update_input()
        self.update_entities(delta_time)
        if not Playfield.OUTSIDE: Playfield.CURRENT_ROOM.update(delta_time)

    def draw(self, surface):
        if Playfield.OUTSIDE:
            for i in range(len(Playfield.ENTITIES)):
                Playfield.ENTITIES[i].draw(surface)
        else:
            Playfield.CURRENT_ROOM.draw(surface)
            Playfield.ENTITIES[0].draw(surface)
