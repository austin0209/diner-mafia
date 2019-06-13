from entities.user.player import Player
from utilities.vector import Vector2
from utilities.color import Color
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera


class Playfield:
    ENTITIES = []

    def __init__(self):
        self.camera = Camera()
        self.camera_location = Vector2(0, 0)
        self.input = Input()
        self.reset()

    def reset(self):
        Playfield.ENTITIES = []
        Playfield.ENTITIES.append(Player(10, 10, 10, 10))

    def update_camera(self):
        self.camera.update()

    def update_input(self):
        self.input.update()

    def update_entities(self, delta_time):
        for i in range(len(Playfield.ENTITIES) - 1, -1, -1):
            Playfield.ENTITIES[i].update(delta_time)

    def update(self, delta_time):
        self.update_camera()
        self.update_input()
        self.update_entities(delta_time)

    def draw(self, surface):
        for i in range(len(Playfield.ENTITIES)):
            Playfield.ENTITIES[i].draw(surface)
