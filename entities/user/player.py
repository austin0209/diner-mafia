from entities.entity import Entity
from entities.geometry.rectangle import Rectangle
from resources.sprite import Sprite
from resources.sprite import Type
from utilities.input import Input
from utilities.input import InputType
from utilities.camera import Camera


class Player(Entity):
    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)
        self.rectangle = Rectangle(self.x, self.y, self.width, self.height)
        self.input = Input()
        self.move_speed = 50
        self.scaled_move_speed = 0

    def set_location(self, x, y):
        super(Player, self).set_location(x, y)
        self.rectangle.set_location(self.x, self.y)

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
        pass

    def update(self, delta_time):
        self.calculate_scaled_move_speed(delta_time)
        self.update_input()
        self.collision()

    def draw(self, surface):
        self.rectangle.draw(surface)
