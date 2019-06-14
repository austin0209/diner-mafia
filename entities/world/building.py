import pygame
from entities.entity import Entity
from entities.world.door import Door
from resources.sprite import Sprite
from resources.sprite import Type
from level.room import Room
from utilities.color import Color

class Building(Entity):

    def __init__(self, x, y, total_floors, id):
        super(Building, self).__init__(x, y, 48, 64)
        self.floors = []
        self.entrance = Door(x + 18, y + 46, 12, 18, id)
        self.room_index = -1
        self.sprite = Sprite(x, y, Type.HOUSE_0)
        for i in range(total_floors):
            self.floors.append(Room(id, i, total_floors, Color.RED if id == 0 else Color.GREEN))

    def update(self, delta_time):
        pass
    
    def draw(self, surface):
        pygame.draw.rect(
            surface,
            (255, 0, 0),
            (
                self.scaled_location().x,
                self.scaled_location().y,
                self.scaled_width(),
                self.scaled_height()
            ),
            int(0)
        )
        self.sprite.draw(surface)
        self.entrance.draw(surface)


