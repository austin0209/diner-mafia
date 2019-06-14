import pygame
from entities.entity import Entity
from entities.world.door import Door
from resources.sprite import Sprite
from resources.sprite import Type
from level.rooms.normal_room import NormalRoom
from level.rooms.special_room import SpecialRoom
from level.rooms.shop_room import ShopRoom
from entities.world.building_type import BuildingType


class Building(Entity):

    def __init__(self, x, y, id, building_type=BuildingType.NORMAL):
        super(Building, self).__init__(x, y, 48, 64)
        self.type = building_type
        self.id = id
        self.floors = []
        self.create_floors()
        self.entrance = None
        self.create_entrance()
        self.sprite = None
        self.create_sprite()
        self.room_index = -1 # TODO: Do I still need this?

    def create_floors(self):
        if self.type == BuildingType.NORMAL:
            self.floors.append(NormalRoom(self.id))
        elif self.type == BuildingType.SPECIAL:
            self.floors.append(SpecialRoom(self.id))
        elif self.type == BuildingType.SHOP:
            self.floors.append(ShopRoom(0, self.id))
            self.floors.append(ShopRoom(1, self.id))

    def create_entrance(self):
        # TODO: Doors are not centered for all sprites
        self.entrance = Door(self.x + 18, self.y + 46, 12, 18, id)

    def create_sprite(self):
        # TODO: Pick different sprites based on building type
        self.sprite = Sprite(self.x, self.y, Type.HOUSE_0)

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


