from level.rooms.room import Room
from utilities.color import Color
from entities.geometry.rectangle import Rectangle


class ShopRoom(Room):
    "A room that has stairs either going up or down"

    def __init__(self, floor_num, building_id):
        super(ShopRoom, self).__init__(building_id)
        self.floor_num = floor_num

    def create_bounds(self):
        self.bounds = Rectangle(0, 0, 18 * 16, 6 * 16)

    def make_exits(self):
        assert self.floor_num == 0 or self.floor_num == 1
        if self.floor_num == 0:
            # Bottom floor, need stairs going up and door to outside
            # Add door: TODO: Door should not be centered
            self.exits.append(Rectangle(self.bounds.x + self.bounds.width / 2 - 16,
                                        self.bounds.y + self.bounds.height - 16, 32, 16, color=Color.BLACK))
            # Add stairs: TODO: Need to decide on location and dimensions of stairs.
            self.exits.append(Rectangle(0, 0, 32, 64))
        else:
            # Top floor, only need stairs going down TODO: Need to decide on location and dimensions of stairs
            self.exits.append(Rectangle(0, 0, 32, 64))

    def update(self, delta_time):
        pass
