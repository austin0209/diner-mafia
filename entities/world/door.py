import pygame
from entities.entity import Entity

class Door(Entity):

    def __init__(self, x, y, id):
        super(Door, self).__init__(x, y, 16, 32)
        self.id = id

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (
                self.scaled_location().x,
                self.scaled_location().y,
                self.scaled_width(),
                self.scaled_height()
            ),
            int(0)
        )