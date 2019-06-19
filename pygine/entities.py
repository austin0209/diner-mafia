import pygine.globals
from enum import IntEnum
from pygame import Rect
from pygine.base import PygineObject
from pygine.draw import draw_rectangle
from pygine.geometry import Rectangle
from pygine.maths import Vector2, distance_between
from pygine.resource import Sprite, SpriteType
from pygine.utilities import CameraType, Color, Input, InputType


class Entity(PygineObject):
    def __init__(self, x=0, y=0, width=1, height=1):
        super(Entity, self).__init__(x, y, width, height)
        self.color = Color.WHITE
        self.layer = 0
        self.remove = False
        self.__bounds_that_actually_draw_correctly = Rectangle(
            self.x, self.y, self.width, self.height, self.color, 2)

    def set_color(self, color):
        self.color = color
        self.__bounds_that_actually_draw_correctly.color = color

    def set_location(self, x, y):
        super(Entity, self).set_location(x, y)
        self.__bounds_that_actually_draw_correctly.set_location(self.x, self.y)

    def update(self, delta_time, entities):
        raise NotImplementedError(
            "A class that inherits Entity did not implement the update(delta_time, entities) method")

    def draw_bounds(self, surface, camera_type):
        self.__bounds_that_actually_draw_correctly.draw(surface, camera_type)

    def draw(self, surface):
        raise NotImplementedError(
            "A class that inherits Entity did not implement the draw(surface) method")


class Direction(IntEnum):
    NONE = 0,
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4


class Kinetic(Entity):
    def __init__(self, x, y, width, height, speed):
        super(Kinetic, self).__init__(x, y, width, height)
        self.velocity = Vector2()
        self.default_move_speed = speed
        self.move_speed = 0
        self.facing = Direction.NONE
        self.collision_rectangles = []
        self.collision_width = 0

    def update_collision_rectangles(self):
        self.collision_width = self.move_speed + 1
        self.collision_rectangles = [
            Rect(self.x + self.collision_width, self.y - self.collision_width,
                 self.width - self.collision_width * 2, self.collision_width),
            Rect(self.x + self.collision_width, self.y + self.height, self.width -
                 self.collision_width * 2, self.collision_width),
            Rect(self.x - self.collision_width, self.y + self.collision_width,
                 self.collision_width, self.height - self.collision_width * 2),
            Rect(self.x + self.width, self.y + self.collision_width,
                 self.collision_width, self.height - self.collision_width * 2)
        ]

    def calculate_scaled_speed(self, delta_time):
        self.move_speed = self.default_move_speed * delta_time

    def collision(self, entities):
        raise NotImplementedError(
            "A class that inherits Kinetic did not implement the collision(surface) method")

    def update(self, delta_time, entities):
        raise NotImplementedError(
            "A class that inherits Kinetic did not implement the update(delta_time, entities) method")

    def draw_collision_rectangles(self, surface):
        for r in self.collision_rectangles:
            draw_rectangle(
                surface,
                r,
                CameraType.DYNAMIC,
                Color.RED,
            )


class Player(Kinetic):
    def __init__(self, x, y):
        super(Player, self).__init__(x, y, 10, 10, 50)
        self.input = Input()
        self.sprite = Sprite(self.x - 3, self.y - 22, SpriteType.PLAYER_F)
        self.shadow = Sprite(self.x - 3, self.y - 21, SpriteType.PLAYER_SHADOW)
        self.set_color(Color.RED)

    def set_location(self, x, y):
        super(Player, self).set_location(x, y)
        self.sprite.set_location(self.x - 3, self.y - 22)
        self.shadow.set_location(self.x - 3, self.y - 21)

    def move(self, direction=Direction.NONE):
        self.facing = direction
        if self.facing == Direction.UP:
            self.sprite.set_sprite(SpriteType.PLAYER_B)
            self.set_location(self.x, self.y - self.move_speed)
            self.velocity.y = -1
        if self.facing == Direction.DOWN:
            self.sprite.set_sprite(SpriteType.PLAYER_F)
            self.set_location(self.x, self.y + self.move_speed)
            self.velocity.y = 1
        if self.facing == Direction.LEFT:
            self.sprite.set_sprite(SpriteType.PLAYER_L)
            self.set_location(self.x - self.move_speed, self.y)
            self.velocity.x = -1
        if self.facing == Direction.RIGHT:
            self.sprite.set_sprite(SpriteType.PLAYER_R)
            self.set_location(self.x + self.move_speed, self.y)
            self.velocity.x = 1

    def update_input(self):
        self.input.update()
        if self.input.pressing(InputType.UP):
            self.move(Direction.UP)
        if self.input.pressing(InputType.DOWN):
            self.move(Direction.DOWN)
        if self.input.pressing(InputType.LEFT):
            self.move(Direction.LEFT)
        if self.input.pressing(InputType.RIGHT):
            self.move(Direction.RIGHT)

    def rectanlge_collision_logic(self, entity):
        # Bottom
        if self.collision_rectangles[0].colliderect(entity.bounds) and self.velocity.y < 0:
            self.set_location(self.x, entity.bounds.bottom)
        # Top
        elif self.collision_rectangles[1].colliderect(entity.bounds) and self.velocity.y > 0:
            self.set_location(self.x, entity.bounds.top - self.bounds.height)
        # Right
        elif self.collision_rectangles[2].colliderect(entity.bounds) and self.velocity.x < 0:
            self.set_location(entity.bounds.right, self.y)
        # Left
        elif self.collision_rectangles[3].colliderect(entity.bounds) and self.velocity.x > 0:
            self.set_location(entity.bounds.left - self.bounds.width, self.y)

    def collision(self, entities):
        for e in entities:
            if (
                isinstance(e, Building) or
                isinstance(e, Tree) or
                isinstance(e, NPC)
            ):
                self.rectanlge_collision_logic(e)

    def update(self, delta_time, entities):
        self.calculate_scaled_speed(delta_time)
        self.update_input()
        self.update_collision_rectangles()
        self.collision(entities)

    def draw(self, surface):
        if pygine.globals.debug:
            self.draw_bounds(surface, CameraType.DYNAMIC)
            self.draw_collision_rectangles(surface)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class NPCType(IntEnum):
    MALE = 0
    FEMALE = 1


class NPC(Entity):
    def __init__(self, x, y, type):
        super(NPC, self).__init__(x, y, 10, 10)
        self.type = type
        if self.type == NPCType.MALE:
            self.sprite = Sprite(self.x - 3, self.y - 22, SpriteType.NPC_M)
        if self.type == NPCType.FEMALE:
            self.sprite = Sprite(self.x - 3, self.y - 22, SpriteType.NPC_F)
        self.shadow = Sprite(self.x - 3, self.y - 21, SpriteType.PLAYER_SHADOW)
        self.speech_bubble = Sprite(
            self.x + 8, self.y - 28, SpriteType.SPEECH_BUBBLE)
        self.radius = 32
        self.show_prompt = False
        self.set_color(Color.RED)

    def set_location(self, x, y):
        super(NPC, self).set_location(x, y)
        self.sprite.set_location(self.x - 3, self.y - 22)
        self.shadow.set_location(self.x - 3, self.y - 21)
        self.speech_bubble.set_height(self.x + 8, self.y - 28)

    def within_radius(self, e):
        if distance_between(self.center, e.center) <= self.radius:
            self.show_prompt = True
        else:
            self.show_prompt = False

    def update_conversation(self, entities):
        for e in entities:
            if isinstance(e, Player):
                self.within_radius(e)

    def update(self, delta_time, entities):
        self.update_conversation(entities)

    def draw(self, surface):
        if pygine.globals.debug:
            self.draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)
        if self.show_prompt:
            self.speech_bubble.draw(surface, CameraType.DYNAMIC)


class Building(Entity):
    def __init__(self, x, y, width, height):
        super(Building, self).__init__(x, y, width, height)
        self.sprite = None
        self.shadow = None

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        if pygine.globals.debug:
            self.draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class SimpleHouse(Building):
    def __init__(self, x, y):
        super(SimpleHouse, self).__init__(x + 4, y + 24, 40, 40)
        self.sprite = Sprite(self.x - 4, self.y - 24, SpriteType.SIMPLE_HOUSE)
        self.set_color(Color.RED)


class SpecialHouse(Building):
    def __init__(self, x, y):
        super(SpecialHouse, self).__init__(x + 4, y + 24, 72, 40)
        self.sprite = Sprite(self.x - 4, self.y - 24, SpriteType.SPECIAL_HOUSE)
        self.shadow = Sprite(self.x - 4 - 16, self.y - 24,
                             SpriteType.SPECIAL_HOUSE_SHADOW)
        self.set_color(Color.RED)


class Tree(Entity):
    def __init__(self, x, y):
        super(Tree, self).__init__(x, y, 10, 10)
        self.sprite = Sprite(self.x - 11, self.y - 21, SpriteType.TREE_THING)
        self.shadow = Sprite(self.x - 11 - 8, self.y - 21,
                             SpriteType.TREE_THING_SHADOW)

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        if pygine.globals.debug:
            self.draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)
