import pygine.globals
from enum import IntEnum
from pygame import Rect
from pygine.base import PygineObject
from pygine.draw import draw_rectangle
from pygine.geometry import Rectangle
from pygine.maths import Vector2, distance_between
from pygine.resource import Sprite, SpriteType
from pygine.utilities import Camera, CameraType, Color, Input, InputType, Timer
from random import randint, random


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

    def _draw_bounds(self, surface, camera_type):
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

    def _update_collision_rectangles(self):
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

    def _calculate_scaled_speed(self, delta_time):
        self.move_speed = self.default_move_speed * delta_time

    def _collision(self, entities):
        raise NotImplementedError(
            "A class that inherits Kinetic did not implement the collision(surface) method")

    def update(self, delta_time, entities):
        raise NotImplementedError(
            "A class that inherits Kinetic did not implement the update(delta_time, entities) method")

    def _draw_collision_rectangles(self, surface):
        for r in self.collision_rectangles:
            draw_rectangle(
                surface,
                r,
                CameraType.DYNAMIC,
                Color.RED,
            )


class Actor(Kinetic):
    def __init__(self, x, y, width, height, speed):
        super(Actor, self).__init__(x, y, width, height, speed)
        self.input = Input()

    def _update_input(self):
        raise NotImplementedError(
            "A class that inherits Actor did not implement the _update_input() method")


class Player(Actor):
    def __init__(self, x, y, width=10, height=10, speed=50):
        super(Player, self).__init__(x, y, width, height, speed)
        self.sprite = Sprite(self.x - 3, self.y - 22, SpriteType.PLAYER_F)
        self.shadow = Sprite(self.x - 3, self.y - 21, SpriteType.PLAYER_SHADOW)
        self.set_color(Color.RED)
        self.item_carrying = Coffee(self.x - 3, self.sprite.y + 8)

    def set_location(self, x, y):
        super(Player, self).set_location(x, y)
        self.sprite.set_location(self.x - 3, self.y - 22)
        self.shadow.set_location(self.x - 3, self.y - 21)

    def _move(self, direction=Direction.NONE):
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

    def _update_input(self):
        self.input.update()
        if self.input.pressing(InputType.UP):
            self._move(Direction.UP)
        if self.input.pressing(InputType.DOWN):
            self._move(Direction.DOWN)
        if self.input.pressing(InputType.LEFT):
            self._move(Direction.LEFT)
        if self.input.pressing(InputType.RIGHT):
            self._move(Direction.RIGHT)

    def _rectangle_collision_logic(self, entity):
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

    def _collision(self, entities):
        for e in entities:
            if (
                isinstance(e, Building) or
                isinstance(e, Furniture) or
                isinstance(e, Wall) or
                isinstance(e, Tree) or
                isinstance(e, NPC)
            ):
                self._rectangle_collision_logic(e)

    def _move_item(self):
        if self.item_carrying != None:
            self.item_carrying.set_location(self.x - 3, self.sprite.y - 8)

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        self._update_input()
        self._update_collision_rectangles()
        self._collision(entities)
        self._move_item()

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
            self._draw_collision_rectangles(surface)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)
            if (self.item_carrying != None):
                self.item_carrying.draw(surface)


class NPCType(IntEnum):
    MALE = 0
    FEMALE = 1


class NPC(Kinetic):
    def __init__(self, x, y, type):
        super(NPC, self).__init__(x, y, 10, 10, 50)
        self.type = type
        if self.type == NPCType.MALE:
            self.sprite = Sprite(self.x - 3, self.y - 22, SpriteType.NPC_M_F)
        if self.type == NPCType.FEMALE:
            self.sprite = Sprite(self.x - 3, self.y - 22, SpriteType.NPC_F_F)
        self.shadow = Sprite(self.x - 3, self.y - 21, SpriteType.PLAYER_SHADOW)
        self.speech_bubble = Sprite(
            self.x - 11, self.y - 32 - 11, SpriteType.SPEECH_BUBBLE)
        self.radius = 32
        self.show_prompt = False
        self.set_color(Color.RED)

    def set_location(self, x, y):
        super(NPC, self).set_location(x, y)
        self.sprite.set_location(self.x - 3, self.y - 22)
        self.shadow.set_location(self.x - 3, self.y - 21)
        self.speech_bubble.set_height(self.x + 8, self.y - 28)

    def _within_radius(self, e):
        if distance_between(self.center, e.center) <= self.radius:
            self.show_prompt = True
        else:
            self.show_prompt = False

    def _update_conversation(self, entities):
        for e in entities:
            if isinstance(e, Player):
                self._within_radius(e)

    def _rectangle_collision_logic(self, entity):
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

    def _collision(self, entities):
        for e in entities:
            if (
                isinstance(e, Building) or
                isinstance(e, Tree)
            ):
                self._rectangle_collision_logic(e)

    def update(self, delta_time, entities):
        self._update_conversation(entities)

        self._calculate_scaled_speed(delta_time)
        # update_MASTER_AI_SYSTEM
        self._update_collision_rectangles()
        self._collision(entities)

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
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
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class SimpleHouse(Building):
    def __init__(self, x, y):
        super(SimpleHouse, self).__init__(x + 4, y + 24 + 10, 40, 40)
        self.sprite = Sprite(self.x - 4, self.y - 24, SpriteType.SIMPLE_HOUSE)
        self.shadow = Sprite(self.x - 4 - 16, self.y - 24,
                             SpriteType.SIMPLE_HOUSE_SHADOW)
        self.set_color(Color.RED)


class SpecialHouse(Building):
    def __init__(self, x, y):
        super(SpecialHouse, self).__init__(x + 4, y + 24 + 10, 72, 40)
        self.sprite = Sprite(self.x - 4, self.y - 24, SpriteType.SPECIAL_HOUSE)
        self.shadow = Sprite(self.x - 4 - 16, self.y - 24,
                             SpriteType.SPECIAL_HOUSE_SHADOW)
        self.set_color(Color.RED)


class Shop(Building):
    def __init__(self, x, y):
        super(Shop, self).__init__(x, y + 64 + 10, 80, 32)
        self.sprite = Sprite(self.x, self.y - 64, SpriteType.SHOP)
        self.shadow = Sprite(self.x - 16, self.y - 64,
                             SpriteType.SHOP_SHADOW)
        self.set_color(Color.RED)


class Diner(Building):
    def __init__(self, x, y):
        super(Diner, self).__init__(x, y + 32, 128, 32)
        self.sprite = Sprite(self.x, self.y - 32, SpriteType.DINER)
        self.shadow = Sprite(self.x - 16, self.y - 32,
                             SpriteType.DINER_SHADOW)
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
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class Furniture(Entity):
    def __init__(self, x, y, width, height):
        super(Furniture, self).__init__(x, y, width, height)
        self.sprite = None

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.sprite.draw(surface, CameraType.DYNAMIC)


class FlowerPot(Furniture):
    def __init__(self, x, y):
        super(FlowerPot, self).__init__(x, y + 10, 16, 16)
        self.sprite = Sprite(self.x, self.y - 32, SpriteType.FLOWER_POT)


class Sofa(Furniture):
    def __init__(self, x, y):
        super(Sofa, self).__init__(x + 4, y + 10, 56, 16)
        self.sprite = Sprite(self.x - 4, self.y - 16, SpriteType.SOFA)


class Bed(Furniture):
    def __init__(self, x, y):
        super(Bed, self).__init__(x, y + 10, 32, 48)
        self.sprite = Sprite(self.x, self.y - 16, SpriteType.BED)


class Shelf(Furniture):
    def __init__(self, x, y, empty=True):
        super(Shelf, self).__init__(x, y + 10, 32, 16)
        if empty:
            self.sprite = Sprite(self.x, self.y - 48, SpriteType.SHELF_EMPTY)
        else:
            self.sprite = Sprite(self.x, self.y - 48, SpriteType.SHELF_FULL)


class CounterShop(Furniture):
    def __init__(self, x, y):
        super(CounterShop, self).__init__(x, y + 10, 112, 16)
        self.sprite = Sprite(self.x, self.y - 32, SpriteType.SHOP_COUNTER)


class CounterDiner(Furniture):
    def __init__(self, x, y):
        super(CounterDiner, self).__init__(x, y + 10 + 4, 240, 12)
        self.sprite = Sprite(self.x, self.y - 80 + 12,
                             SpriteType.DINER_COUNTER)


class StoolTall(Furniture):
    def __init__(self, x, y):
        super(StoolTall, self).__init__(x, y + 10 + 6, 16, 6)
        self.sprite = Sprite(self.x, self.y - 16 - 6, SpriteType.STOOL_TALL)


class StoolShort(Furniture):
    def __init__(self, x, y):
        super(StoolShort, self).__init__(x, y + 10 + 4, 16, 6)
        self.sprite = Sprite(self.x, self.y - 16 - 4, SpriteType.STOOL_SHORT)


class Table(Furniture):
    def __init__(self, x, y):
        super(Table, self).__init__(x, y + 10, 32, 12)
        self.sprite = Sprite(self.x, self.y - 16, SpriteType.TABLE)


class Wall(Entity):
    def __init__(self, x, y, width, height):
        super(Wall, self).__init__(
            x * 16, y * 16 + 10, width * 16, height * 16)
        self.set_color(Color.BLUE)

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)


class ItemType(IntEnum):
    COFFEE = 0
    FISH = 1
    CROP = 2
    EGGS = 3


class Item(Entity):
    def __init__(self, x, y):
        super(Item, self).__init__(x, y, 16, 16)
        self._processed = False
        self._type = None
        self._sprite = None

    def set_location(self, x, y):
        super(Item, self).set_location(x, y)
        self._sprite.set_location(self.x, self.y)

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        self._sprite.draw(surface, CameraType.DYNAMIC)


class Coffee(Item):
    def __init__(self, x, y):
        super(Coffee, self).__init__(x, y)
        self._type = ItemType.COFFEE
        self._sprite = Sprite(x, y, SpriteType.COFFEE_RAW)


class Fish(Item):
    def __init__(self, x, y):
        super(Fish, self).__init__(x, y)
        self._type = ItemType.FISH
        self._sprite = Sprite(x, y, SpriteType.FISH_RAW)


class Crop(Item):
    def __init__(self, x, y):
        super(Crop, self).__init__(x, y)
        self._type = ItemType.CROP
        self._sprite = Sprite(x, y, SpriteType.COFFEE_RAW)


class Eggs(Item):
    def __init__(self, x, y):
        super(Eggs, self).__init__(x, y)
        self._type = ItemType.EGGS
        self._sprite = Sprite(x, y, SpriteType.EGGS_RAW)


###################################################################
#
#   Coffee minigame stuff starts here!
#
###################################################################

class Boat(Actor):
    def __init__(self, x, y, beans=30):
        super(Boat, self).__init__(x, y, 83, 16, 50)
        self.beans = beans
        self.playbounds = Rectangle(
            0, 16 * 4, Camera.BOUNDS.width * .6, 16 * 6 + 20)
        self.sprite = Sprite(x - 16, y - 32, SpriteType.BOAT)

    def set_location(self, x, y):
        super(Boat, self).set_location(x, y)
        self.sprite.set_location(self.x - 16, self.y - 32)

    def _collision(self, entities):
        for e in entities:
            if isinstance(e, Octopus):
                for b in e.bullets:
                    if self.bounds.colliderect(b.bounds):
                        b.dead = True
                        self.beans -= 5
        self.__bounds_collision()

    def _move(self, direction=Direction.NONE):
        self.facing = direction
        if self.facing == Direction.UP:
            self.set_location(self.x, self.y - self.move_speed)
            self.velocity.y = -1
        if self.facing == Direction.DOWN:
            self.set_location(self.x, self.y + self.move_speed)
            self.velocity.y = 1
        if self.facing == Direction.LEFT:
            self.set_location(self.x - self.move_speed, self.y)
            self.velocity.x = -1
        if self.facing == Direction.RIGHT:
            self.set_location(self.x + self.move_speed, self.y)
            self.velocity.x = 1

    def _update_input(self):
        self.input.update()
        if self.input.pressing(InputType.UP):
            self._move(Direction.UP)
        if self.input.pressing(InputType.DOWN):
            self._move(Direction.DOWN)
        if self.input.pressing(InputType.LEFT):
            self._move(Direction.LEFT)
        if self.input.pressing(InputType.RIGHT):
            self._move(Direction.RIGHT)

    def __bounds_collision(self):
        if self.x < self.playbounds.x:
            self.x = self.playbounds.x
        elif self.x + self.width > self.playbounds.x + self.playbounds.width:
            self.x = self.playbounds.x + self.playbounds.width - self.width

        if self.y < self.playbounds.y:
            self.y = self.playbounds.y
        elif self.y + self.height > self.playbounds.y + self.playbounds.height:
            self.y = self.playbounds.y + self.playbounds.height - self.height

    def __check_death(self):
        if self.beans <= 0:
            # TODO: death logic here, maybe display transition and change scene?
            pass

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        self._update_input()
        self._collision(entities)
        self.__check_death()

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            # self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class Octopus(Kinetic):
    def __init__(self, x, y):
        super(Octopus, self).__init__(x, y, 10, 10, randint(10, 30))
        self.timer = Timer(randint(1500, 3000), True)
        self.sprite = Sprite(x - 16, y - 16, SpriteType.OCTOPUS)
        self.bullets = []

    def set_location(self, x, y):
        super(Octopus, self).set_location(x, y)
        self.sprite.set_location(self.x - 16, self.y - 16)

    def __shoot(self):
        self.bullets.append(Bullet(self.x, self.y + self.height / 2))

    def __move(self, entities):
        self.set_location(self.x - self.move_speed, self.y)
        for e in entities:
            if isinstance(e, Boat):
                if self.x < Camera.BOUNDS.width * .6 and self.x > e.x:
                    if self.y < e.y:
                        self.set_location(self.x, self.y + self.move_speed / 4)
                    elif self.y > e.y:
                        self.set_location(self.x, self.y - self.move_speed / 4)

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        self.__move(entities)
        self.timer.update()
        if self.timer.done:
            if random() < 0.25:
                self.__shoot()
            self.timer.reset()
            self.timer.start()
        for b in self.bullets:
            b.update(delta_time, entities)
            if b.dead:
                self.bullets.remove(b)

    def draw(self, surface):
        # Temporary:
        for b in self.bullets:
            b.draw(surface)
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            # self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class Bullet(Kinetic):
    def __init__(self, x, y, speed=50):
        super(Bullet, self).__init__(x, y, 11, 12, speed)
        self.sprite = Sprite(x, y - 2, SpriteType.INK_BULLET)
        self.dead = False

    def set_location(self, x, y):
        super(Bullet, self).set_location(x, y)
        self.sprite.set_location(self.x, self.y - 2)

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        self.set_location(self.x - self.move_speed, self.y)
        if self.x + self.width < Camera.BOUNDS.x:
            self.dead = True

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.sprite.draw(surface, CameraType.DYNAMIC)


###################################################################
#
#   Crop minigame stuff starts here!
#
###################################################################

class Mole(Entity):
    pass


class Mallet(Entity):
    pass
