import pygame
from entities.entity import Entity
from utilities.color import Color
from utilities.camera import Camera


class Rectangle(Entity):
    def __init__(self, x=0, y=0, width=1, height=1, thickness=0, color=Color.WHITE):
        super(Rectangle, self).__init__(x, y, width, height)
        self.thickness = thickness
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (
                self.scaled_location().x,
                self.scaled_location().y,
                self.scaled_width(),
                self.scaled_height()
            ),
            int(self.thickness * Camera.SCALE)
        )
