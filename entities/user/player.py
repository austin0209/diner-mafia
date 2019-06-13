from entities.entity import Entity
from entities.geometry.rectangle import Rectangle
from entities.world.door import Door
from entities.world.building import Building
from resources.sprite import Sprite
from resources.sprite import Type
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera
from level.room import Room


class Player(Entity):
    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)
        self.rectangle = Rectangle(self.x, self.y, self.width, self.height)
        self.input = Input()
        self.move_speed = 50
        self.scaled_move_speed = 0
        print("WHJS")

    def set_location(self, x, y):
        super(Player, self).set_location(x, y)
        self.rectangle.set_location(self.x, self.y)
        print("hello")

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
            for i in range(len(Playfield.ENTITIES)):
                if Playfield.ENTITIES[i] != self:
                    if isinstance(Playfield.ENTITIES[i], Building):
                        if self.bounds.colliderect(Playfield.ENTITIES[i].entrance.bounds):
                            Playfield.OUTSIDE = False
                            Playfield.CURRENT_ROOM = Playfield.ENTITIES[i].floors[0]
                            Playfield.ENTITIES[i].room_index = 0
                            self.set_location(
                                Camera.BOUNDS.width / 2 - self.width / 2, Camera.BOUNDS.height - self.height - 16)
        else:
            room = Playfield.CURRENT_ROOM
            if room.exit != None and self.bounds.colliderect(room.exit.bounds):
                Playfield.OUTSIDE = True
                target_building = Playfield.BUILDINGS[Playfield.CURRENT_ROOM.building_id]
                self.set_location(target_building.x + target_building.bounds.width / 2 - self.width / 2,
                                    target_building.y + target_building.bounds.height)
                Playfield.CURRENT_ROOM = None
            elif room.stair_down != None and self.bounds.colliderect(room.stair_down.bounds):
                Playfield.CURRENT_ROOM = Playfield.BUILDINGS[Playfield.CURRENT_ROOM.building_id].floors[room.floor_num - 1]
                self.set_location(Camera.BOUNDS.width - 64 - 16, 32)
            elif room.stair_up != None and self.bounds.colliderect(room.stair_up.bounds):
                Playfield.CURRENT_ROOM = Playfield.BUILDINGS[Playfield.CURRENT_ROOM.building_id].floors[room.floor_num + 1]
                self.set_location(64 + 16, 32)

    def update(self, delta_time):
        self.calculate_scaled_move_speed(delta_time)
        self.update_input()
        self.collision()

    def draw(self, surface):
        self.rectangle.draw(surface)
