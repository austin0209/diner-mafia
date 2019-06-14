import math
from entities.entity import Entity
from entities.geometry.rectangle import Rectangle
from entities.world.door import Door
from entities.world.building import Building
from entities.npcs.npc import Npc
from entities.world.resourcehub import ResourceHub
from resources.sprite import Sprite
from resources.sprite import Type
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera
from utilities.vector import Vector2
from level.room import Room


class Player(Entity):
    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)
        self.rectangle = Rectangle(self.x, self.y, self.width, self.height)
        self.input = Input()
        self.move_speed = 50
        self.scaled_move_speed = 0
        self.resources = [0, 0, 0, 0]
        self.sprite = Sprite(x, y, Type.PLAYER)

    def set_location(self, x, y):
        super(Player, self).set_location(x, y)
        self.rectangle.set_location(self.x, self.y)
        self.sprite.set_location(self.x, self.y)

    def calculate_scaled_move_speed(self, delta_time):
        self.scaled_move_speed = self.move_speed * delta_time

    def update_input(self):
        self.input.update()
        if self.input.pressing(InputType.UP):
            self.set_location(self.x, self.y - self.scaled_move_speed)
        if self.input.pressing(InputType.DOWN):
            self.set_location(self.x, self.y + self.scaled_move_speed)
        if self.input.pressing(InputType.LEFT):
            self.set_location(self.x - self.scaled_move_speed, self.y)
        if self.input.pressing(InputType.RIGHT):
            self.set_location(self.x + self.scaled_move_speed, self.y)

    def collision(self):
        from level.playfield import Playfield
        if Playfield.OUTSIDE:
            self.outside_collision()
        else:
            self.stair_collision()

    def distance_from(self, other):
        center = Vector2(self.x + self.width / 2, self.y + self.height / 2)
        a = center.x - other.x
        b = center.y - other.y
        return math.sqrt(a * a + b * b)

    def outside_collision(self):
        from level.playfield import Playfield
        for i in range(len(Playfield.ENTITIES)):
            if Playfield.ENTITIES[i] != self:
                if isinstance(Playfield.ENTITIES[i], Building):
                    self.building_collision(Playfield.ENTITIES[i])
                elif isinstance(Playfield.ENTITIES[i], Npc):
                    Playfield.ENTITIES[i].talking = self.distance_from(
                        Playfield.ENTITIES[i].center()) < Npc.PROXIMITY
                elif isinstance(Playfield.ENTITIES[i], ResourceHub):
                    self.resource_collision(Playfield.ENTITIES[i])

    def resource_collision(self, hub):
        if self.bounds.colliderect(hub.bounds):
            self.resources[hub.id] += 1

    def building_collision(self, building):
        from level.playfield import Playfield
        if self.bounds.colliderect(building.entrance.bounds):
            Playfield.OUTSIDE = False
            Playfield.CURRENT_ROOM = building.floors[0]
            building.room_index = 0
            self.set_location(
                Playfield.CURRENT_ROOM.bounds.width / 2 - self.width / 2,
                Playfield.CURRENT_ROOM.bounds.height - self.height - 16)

    def stair_collision(self):
        from level.playfield import Playfield
        room = Playfield.CURRENT_ROOM
        if room.exit != None and self.bounds.colliderect(room.exit.bounds):
            Playfield.OUTSIDE = True
            target_building = Playfield.BUILDINGS[Playfield.CURRENT_ROOM.building_id]
            self.set_location(target_building.x + target_building.bounds.width / 2 - self.width / 2,
                              target_building.y + target_building.bounds.height)
            Playfield.CURRENT_ROOM = None
        elif room.stair_down != None and self.bounds.colliderect(room.stair_down.bounds):
            Playfield.CURRENT_ROOM = Playfield.BUILDINGS[
                Playfield.CURRENT_ROOM.building_id].floors[room.floor_num - 1]
            self.set_location(Camera.BOUNDS.width - 64 - 16, 32)
        elif room.stair_up != None and self.bounds.colliderect(room.stair_up.bounds):
            Playfield.CURRENT_ROOM = Playfield.BUILDINGS[
                Playfield.CURRENT_ROOM.building_id].floors[room.floor_num + 1]
            self.set_location(64 + 16, 32)

    def update(self, delta_time):
        self.calculate_scaled_move_speed(delta_time)
        self.update_input()
        self.collision()
        print(self.resources)

    def draw(self, surface):
        self.rectangle.draw(surface)
        self.sprite.draw(surface)
