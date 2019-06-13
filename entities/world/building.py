import pygame
from entities.entity import Entity
from entities.world.door import Door
from level.room import Room
from utilities.color import Color

class Building(Entity):

    def __init__(self, x, y, total_floors, id):
        super(Building, self).__init__(x, y, 100, 100)
        self.floors = []
        self.entrance = Door(self.x + self.width / 2 - 8, self.y + self.height - 32, id)
        self.room_index = -1

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
        self.entrance.draw(surface)


