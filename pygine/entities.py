import math
import pygine.globals
from enum import IntEnum
from pygame import Rect
from pygine.base import PygineObject
from pygine.draw import draw_rectangle, draw_line
from pygine.geometry import Rectangle
from pygine.maths import Vector2, distance_between
from pygine.resource import Animation, Sprite, SpriteType
from pygine.utilities import Camera, CameraType, Color, Input, InputType, Timer
from random import randint, random


class Entity(PygineObject):
    def __init__(self, x=0, y=0, width=1, height=1):
        super(Entity, self).__init__(x, y, width, height)
        self.sprite = Sprite(x, y, SpriteType.NONE)
        self.color = Color.WHITE
        self.layer = 0
        self.remove = False
        self.ignore = False
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
        self.arms = Sprite(self.x - 3, self.y - 22,
                           SpriteType.PLAYER_ARM_SIDE_F)
        self.shadow = Sprite(self.x - 3, self.y - 21, SpriteType.PLAYER_SHADOW)
        self.set_color(Color.RED)
        self.item_carrying = None
        self.animation_walk = Animation(6, 6, 100)
        self.walking = False

    def set_location(self, x, y):
        super(Player, self).set_location(x, y)
        self.sprite.set_location(self.x - 3, self.y - 22)
        self.arms.set_location(self.x - 3, self.y - 22)
        self.shadow.set_location(self.x - 3, self.y - 21)

        if self.item_carrying != None:
            self.item_carrying.set_location(self.x - 3, self.sprite.y - 8)

    def _move(self, direction=Direction.NONE):
        self.facing = direction
        self.walking = True
        if self.facing == Direction.UP:
            self.sprite.set_sprite(SpriteType.PLAYER_B)
            self.arms.set_sprite(SpriteType.PLAYER_ARM_SIDE_B)
            self.set_location(self.x, self.y - self.move_speed)
            self.velocity.y = -1
        if self.facing == Direction.DOWN:
            self.sprite.set_sprite(SpriteType.PLAYER_F)
            self.arms.set_sprite(SpriteType.PLAYER_ARM_SIDE_F)
            self.set_location(self.x, self.y + self.move_speed)
            self.velocity.y = 1
        if self.facing == Direction.LEFT:
            self.sprite.set_sprite(SpriteType.PLAYER_L)
            self.arms.set_sprite(SpriteType.PLAYER_ARM_SIDE_L)
            self.set_location(self.x - self.move_speed, self.y)
            self.velocity.x = -1
        if self.facing == Direction.RIGHT:
            self.sprite.set_sprite(SpriteType.PLAYER_R)
            self.arms.set_sprite(SpriteType.PLAYER_ARM_SIDE_R)
            self.set_location(self.x + self.move_speed, self.y)
            self.velocity.x = 1

    def _update_input(self, delta_time):
        self.input.update(delta_time)
        self.walking = False
        if self.input.pressing(InputType.UP) and not self.input.pressing(InputType.DOWN):
            self._move(Direction.UP)
        if self.input.pressing(InputType.DOWN) and not self.input.pressing(InputType.UP):
            self._move(Direction.DOWN)
        if self.input.pressing(InputType.LEFT) and not self.input.pressing(InputType.RIGHT):
            self._move(Direction.LEFT)
        if self.input.pressing(InputType.RIGHT) and not self.input.pressing(InputType.LEFT):
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
                    not e.ignore and
                    (
                        isinstance(e, Building) or
                        isinstance(e, Furniture) or
                        isinstance(e, Wall) or
                        isinstance(e, Tree)
                    )
                    # isinstance(e, NPC)
            ):
                self._rectangle_collision_logic(e)

    def _update_animation(self, delta_time):
        if self.walking:
            self.animation_walk.update(delta_time)
            self.sprite.set_frame(
                self.animation_walk.current_frame, self.animation_walk.columns)
            self.arms.set_frame(
                self.animation_walk.current_frame, self.animation_walk.columns)
        else:
            self.sprite.set_frame(0, self.animation_walk.columns)
            self.arms.set_frame(0, self.animation_walk.columns)

    def _update_item(self):
        if self.item_carrying != None:
            self.arms.increment_sprite_x(16 * 6)

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        self._update_input(delta_time)
        self._update_collision_rectangles()
        self._collision(entities)
        self._update_animation(delta_time)
        self._update_item()

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
            self._draw_collision_rectangles(surface)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)
            self.arms.draw(surface, CameraType.DYNAMIC)
            if (self.item_carrying != None):
                self.item_carrying.draw(surface)


class SpeechBubble(Entity):
    def __init__(self, x, y, source, sprite_type=SpriteType.NONE):
        super(SpeechBubble, self).__init__(x, y, 1, 1)
        self.sprite = Sprite(x, y, SpriteType.SPEECH_BUBBLE)
        self.__content = Sprite(x + 8, y + 8, sprite_type)
        self.source = source

    def set_location(self, x, y):
        super(SpeechBubble, self).set_location(x, y)
        self.sprite.set_location(x, y)
        self.__content.set_location(x + 8, y + 8)

    def set_content(self, sprite_type):
        self.__content.set_sprite(sprite_type)
        self.__content.set_location(self.x + 8, self.y + 8)

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        self.sprite.draw(surface, CameraType.DYNAMIC)
        self.__content.draw(surface, CameraType.DYNAMIC)


class NPCType(IntEnum):
    MALE = 0
    FEMALE = 1


class NPC(Kinetic):
    def __init__(self, x, y, type, can_move=True, horizontal=True, start_direction=1, walk_duration=5000):
        super(NPC, self).__init__(x, y, 10, 10, 25)
        self.type = type
        self.sprite = Sprite(self.x - 3, self.y - 22, SpriteType.NONE)
        self.shadow = Sprite(self.x - 3, self.y - 21, SpriteType.PLAYER_SHADOW)
        self.speech_bubble = SpeechBubble(self.x - 11, self.y - 32 - 11, self)
        self.radius = 32
        self.show_prompt = False
        self.set_color(Color.RED)
        self.walk_direction = 1 if start_direction >= 0 else -1
        self.horizontal = horizontal
        self.can_move = can_move
        self._walk_timer = Timer(walk_duration, True)
        self.animation_walk = Animation(6, 6, 100)
        self.walking = True
        self._set_walking_sprite()
        self._set_random_emotion()

    def set_location(self, x, y):
        super(NPC, self).set_location(x, y)
        self.sprite.set_location(self.x - 3, self.y - 22)
        self.shadow.set_location(self.x - 3, self.y - 21)
        self.speech_bubble.set_location(self.x - 11, self.y - 32 - 11)

    def _set_random_emotion(self):
        rand = randint(1, 4)
        if rand == 1:
            self.speech_bubble.set_content(SpriteType.FACE_HAPPY)
        elif rand == 2:
            self.speech_bubble.set_content(SpriteType.FACE_SAD)
        elif rand == 3:
            self.speech_bubble.set_content(SpriteType.FACE_MAD)
        elif rand == 4:
            self.speech_bubble.set_content(SpriteType.FACE_SURPRISED)

    def _stop_walking(self):
        if not self.horizontal:
            if self.type == NPCType.MALE:
                self.sprite.set_sprite(SpriteType.NPC_M_F)
            else:
                self.sprite.set_sprite(SpriteType.NPC_F_F)
        self._set_random_emotion()
        self.walking = not self.walking

    def _walk(self, delta_time):
        self._walk_timer.update(delta_time)
        if self._walk_timer.done:
            if random() < 0.25:
                self._stop_walking()
            if self.walking:
                self.walk_direction = -self.walk_direction
                self._set_walking_sprite()
            self._walk_timer.reset()
            self._walk_timer.start()
        if self.walking:
            if self.horizontal:
                self.set_location(self.x + self.move_speed *
                                  self.walk_direction, self.y)
            else:
                self.set_location(
                    self.x, self.y + self.move_speed * self.walk_direction)

    def _set_walking_sprite(self):
        if self.can_move:
            if self.horizontal:
                if self.walk_direction > 0:
                    if self.type == NPCType.MALE:
                        self.sprite.set_sprite(SpriteType.NPC_M_R)
                    else:
                        self.sprite.set_sprite(SpriteType.NPC_F_R)
                else:
                    if self.type == NPCType.MALE:
                        self.sprite.set_sprite(SpriteType.NPC_M_L)
                    else:
                        self.sprite.set_sprite(SpriteType.NPC_F_L)
            else:
                if self.walk_direction > 0:
                    if self.type == NPCType.MALE:
                        self.sprite.set_sprite(SpriteType.NPC_M_F)
                    else:
                        self.sprite.set_sprite(SpriteType.NPC_F_F)
                else:
                    if self.type == NPCType.MALE:
                        self.sprite.set_sprite(SpriteType.NPC_M_B)
                    else:
                        self.sprite.set_sprite(SpriteType.NPC_F_B)
        else:
            if self.type == NPCType.MALE:
                self.sprite.set_sprite(SpriteType.NPC_M_F)
            else:
                self.sprite.set_sprite(SpriteType.NPC_F_F)

    def _within_radius(self, e):
        if distance_between(self.center, e.center) <= self.radius:
            self.show_prompt = True
        else:
            self.show_prompt = False

    def _update_conversation(self, entities):
        for e in entities:
            if isinstance(e, Player):
                last = self.show_prompt
                self._within_radius(e)
                if last != self.show_prompt:
                    if self.show_prompt:
                        entities.append(self.speech_bubble)
                    else:
                        entities.remove(self.speech_bubble)

    def _update_animation(self, delta_time):
        if self.walking:
            self.animation_walk.update(delta_time)
            self.sprite.set_frame(
                self.animation_walk.current_frame, self.animation_walk.columns)
        else:
            self.sprite.set_frame(0, self.animation_walk.columns)

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
        if self.can_move:
            self._walk(delta_time)

        # self._update_collision_rectangles()
        # self._collision(entities)

        if self.can_move:
            self._update_animation(delta_time)

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class Merchant(NPC):
    def __init__(self, x, y, type, speech_content):
        super(Merchant, self).__init__(x, y, type, can_move=False)
        self.speech_bubble.set_content(speech_content)

    def _update_conversation(self, entities):
        for e in entities:
            if isinstance(e, Player):
                last = self.show_prompt
                self._within_radius(e)
                if last != self.show_prompt:
                    if self.show_prompt:
                        entities.append(self.speech_bubble)
                    else:
                        entities.remove(self.speech_bubble)


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
        super(SimpleHouse, self).__init__(x + 4, y + 24, 40, 40)
        self.sprite = Sprite(self.x - 4, self.y - 24, SpriteType.SIMPLE_HOUSE)
        self.shadow = Sprite(self.x - 4 - 16, self.y - 24,
                             SpriteType.SIMPLE_HOUSE_SHADOW)
        self.set_color(Color.RED)


class SpecialHouse(Building):
    def __init__(self, x, y):
        super(SpecialHouse, self).__init__(x + 4, y + 24, 72, 40)
        self.sprite = Sprite(self.x - 4, self.y - 24, SpriteType.SPECIAL_HOUSE)
        self.shadow = Sprite(self.x - 4 - 16, self.y - 24,
                             SpriteType.SPECIAL_HOUSE_SHADOW)
        self.set_color(Color.RED)


class Shop(Building):
    def __init__(self, x, y):
        super(Shop, self).__init__(x, y + 64, 80, 32)
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
        super(Tree, self).__init__(x, y, 20, 20)
        self.sprite = Sprite(self.x - 11 - 16, self.y -
                             21, SpriteType.TREE_CLUSTER)
        # self.shadow = Sprite(self.x - 11 - 8, self.y - 21,
        #                     SpriteType.TREE_THING_SHADOW)

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            # self.shadow.draw(surface, CameraType.DYNAMIC)
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
        super(CounterDiner, self).__init__(x, y + 10 + 2, 256, 12)
        self.sprite = Sprite(self.x, self.y - 80 + 12,
                             SpriteType.DINER_COUNTER)


class StoolTall(Furniture):
    def __init__(self, x, y):
        super(StoolTall, self).__init__(x, y + 10, 16, 6)
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

    def apply_an_offset(self, x_offset, y_offset):
        self.set_location(self.x + x_offset, self.y + y_offset)

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
    def __init__(self, x, y, value):
        super(Item, self).__init__(x, y, 16, 16)
        self._processed = False
        self._type = None
        self._sprite = None
        self.value = value

    def set_location(self, x, y):
        super(Item, self).set_location(x, y)
        self._sprite.set_location(self.x, self.y)

    def update(self, delta_time, entities):
        pass

    def draw(self, surface):
        self._sprite.draw(surface, CameraType.DYNAMIC)


class Coffee(Item):
    def __init__(self, x, y, value):
        super(Coffee, self).__init__(x, y, value)
        self._type = ItemType.COFFEE
        self._sprite = Sprite(x, y, SpriteType.COFFEE_RAW)


class Fish(Item):
    def __init__(self, x, y, value):
        super(Fish, self).__init__(x, y, value)
        self._type = ItemType.FISH
        self._sprite = Sprite(x, y, SpriteType.FISH_RAW)


class Crop(Item):
    def __init__(self, x, y, value):
        super(Crop, self).__init__(x, y, value)
        self._type = ItemType.CROP
        self._sprite = Sprite(x, y, SpriteType.CROP_RAW)


class Eggs(Item):
    def __init__(self, x, y, value):
        super(Eggs, self).__init__(x, y, value)
        self._type = ItemType.EGGS
        self._sprite = Sprite(x, y, SpriteType.EGGS_RAW)


class SellPad(Entity):
    def __init__(self, x, y, width, height, direction=Direction.UP):
        super(SellPad, self).__init__(x, y, width, height)
        self.direction = direction

    def __collision(self, entities):
        for e in entities:
            if e.bounds.colliderect(self.bounds):
                if isinstance(e, Player) and e.item_carrying is not None:
                    if e.input.pressing(InputType.A) and int(e.facing) == int(self.direction):
                        pygine.globals.money += e.item_carrying.value
                        e.item_carrying = None

    def update(self, delta_time, entities):
        self.__collision(entities)

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)


###################################################################
#
#   Coffee minigame stuff starts here!
#
###################################################################

class Boat(Actor):
    def __init__(self, x, y, beans=50):
        super(Boat, self).__init__(x, y, 83, 16, 50)
        self.beans = beans
        self.playbounds = Rectangle(
            0, 16 * 3, Camera.BOUNDS.width, Camera.BOUNDS.height - 16 * 3)
        self.sprite = Sprite(x - 16, y - 48, SpriteType.BOAT)
        self.shadow = Sprite(x - 16 - 16, y - 16, SpriteType.BOAT_SHADOW)
        self.blinks = 5
        self.invis_duration = 1600
        self.invis_timer = Timer(self.invis_duration)
        self.blink_timer = Timer(self.invis_duration / self.blinks / 2)
        self.damaged = False
        self.flashing = False
        self.dead = False

    def set_location(self, x, y):
        super(Boat, self).set_location(x, y)
        self.sprite.set_location(self.x - 16, self.y - 48)
        self.shadow.set_location(self.x - 16 - 16, self.y - 16)

    def _collision(self, entities):
        for e in entities:
            if not self.damaged:
                if isinstance(e, Bullet) or isinstance(e, Octopus):
                    if self.bounds.colliderect(e.bounds):
                        e.dead = True
                        self.__decrease_health(5)
                elif isinstance(e, Rock):
                    if self.bounds.colliderect(e.bounds):
                        self.__decrease_health(10)
        self.__bounds_collision()

    def __decrease_health(self, amount):
        self.damaged = True
        self.beans -= amount
        self.invis_timer.start()
        self.blink_timer.start()
        self.sprite.set_sprite(SpriteType.BOAT_OWO)

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

    def _update_input(self, delta_time):
        self.input.update(delta_time)
        if self.input.pressing(InputType.UP):
            self._move(Direction.UP)
        if self.input.pressing(InputType.DOWN):
            self._move(Direction.DOWN)
        if self.input.pressing(InputType.LEFT):
            self._move(Direction.LEFT)
        if self.input.pressing(InputType.RIGHT):
            self._move(Direction.RIGHT)

    def __update_health(self, delta_time):
        if self.damaged:
            self.invis_timer.update(delta_time)
            self.blink_timer.update(delta_time)
            if self.blink_timer.done:
                self.flashing = not self.flashing
                self.blink_timer.reset()
                self.blink_timer.start()
            if self.invis_timer.done:
                self.damaged = False
                self.flashing = False
                self.invis_timer.reset()
                self.sprite.set_sprite(SpriteType.BOAT)

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
            self.dead = True

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)

        if self.dead:
            self.flashing = False
            self.set_location(self.x - self.move_speed / 2 + randint(-2, 0), self.y + self.move_speed)
            return

        self._update_input(delta_time)
        self._collision(entities)
        self.__update_health(delta_time)
        self.__check_death()

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            if not self.flashing:
                self.shadow.draw(surface, CameraType.DYNAMIC)
                self.sprite.draw(surface, CameraType.DYNAMIC)


class Octopus(Kinetic):
    def __init__(self, x, y):
        super(Octopus, self).__init__(x, y, 16, 16, randint(10, 30))
        self.timer = Timer(randint(1, 5) * 1000, True)
        self.sprite = Sprite(x - 16, y - 16, SpriteType.OCTOPUS)
        self.shadow = Sprite(x - 16 - 8, y - 16 + 16,
                             SpriteType.OCTOPUS_SHADOW)
        self.i = 0

    def set_location(self, x, y):
        super(Octopus, self).set_location(x, y)
        self.sprite.set_location(self.x - 16, self.y - 16)
        self.shadow.set_location(self.x - 16 - 8, self.y - 16 + 16)

    def __shoot(self, entities):
        entities.append(Bullet(self.x, self.y + self.height / 2, 200))

    def __move(self, delta_time):
        self.i += 1 * delta_time
        self.set_location(
            self.x - self.move_speed,
            self.y + math.sin(self.i)
        )

    def update(self, delta_time, entities):        
        self._calculate_scaled_speed(delta_time)
        self.__move(delta_time)
        self.timer.update(delta_time)
        if self.timer.done:
            if randint(1, 10) <= 7:
                self.__shoot(entities)
            self.timer.reset()
            self.timer.start()

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class Bullet(Kinetic):
    def __init__(self, x, y, speed=50):
        super(Bullet, self).__init__(x, y, 11, 12, speed)
        self.sprite = Sprite(x, y - 2, SpriteType.INK_BULLET)
        self.shadow = Sprite(x, y - 2 + 16, SpriteType.INK_BULLET_SHADOW)
        self.dead = False

    def set_location(self, x, y):
        super(Bullet, self).set_location(x, y)
        self.sprite.set_location(self.x, self.y - 2)
        self.shadow.set_location(self.x, self.y - 2 + 16)

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        self.set_location(self.x - self.move_speed, self.y)

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)


class Rock(Kinetic):
    def __init__(self, x, y, speed=75):
        super(Rock, self).__init__(x, y, 34, 14, speed)
        self.sprite = Sprite(x - 7, y - 16, SpriteType.ROCK)
        self.shadow = Sprite(self.x - 7 - 8, self.y -
                             16, SpriteType.ROCK_SHADOW)
        self.dead = False

    def set_location(self, x, y):
        super(Rock, self).set_location(x, y)
        self.sprite.set_location(self.x - 7, self.y - 16)
        self.shadow.set_location(self.x - 7 - 8, self.y - 16)

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        self.set_location(self.x - self.move_speed, self.y)

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
        else:
            self.shadow.draw(surface, CameraType.DYNAMIC)
            self.sprite.draw(surface, CameraType.DYNAMIC)

class SandWall(Entity):
    def __init__(self, x, y, layer, total_layers):
        super(SandWall, self).__init__(x, y - layer * 10, 64, 32)
        self.layer = layer
        self.sprite = Sprite(
            self.x, self.y, SpriteType.SAND_WALL)

        self.direction = 1
        self.parallax_layers = total_layers
        self.parallax_variance = 10
        self.parallax_speed = 0
        self.calculate_parallax_speed()

    def set_location(self, x, y):
        super(SandWall, self).set_location(x, y)
        self.sprite.set_location(self.x, self.y)

    def set_direction(self, direction):
        self.direction = direction
        self.calculate_parallax_speed()

    def calculate_parallax_speed(self):
        assert (self.parallax_variance > 0), \
            "Parallax Variance must be greater than zero!"
        self.parallax_speed = self.parallax_variance * \
            (self.parallax_layers - (self.layer + 1))**2 * self.direction * -1
        if self.parallax_speed == 0:
            self.parallax_speed = self.parallax_variance / 2 * self.direction * -1

    def update_parallax(self, delta_time):        
        self.set_location(self.x + self.parallax_speed * delta_time, self.y)

    def update(self, delta_time, entities):
        self.update_parallax(delta_time)

    def draw(self, surface):
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


###################################################################
#
#   Fish minigame stuff starts here!
#
###################################################################

class Hook(Actor):
    def __init__(self, ocean_depth):
        super(Hook, self).__init__(0, 0, 13, 13, 80)
        self.ocean_depth = ocean_depth
        self.sprite = Sprite(self.x, self.y - 7, SpriteType.HOOK)
        self.direction = 1
        self.total_hooked_fish = 0

    def set_location(self, x, y):
        super(Hook, self).set_location(x, y)
        self.sprite.set_location(self.x, self.y - 7)

    def __bounds_collision(self):
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > Camera.BOUNDS.width:
            self.x = Camera.BOUNDS.width - self.width

    def _collision(self, entities):
        if self.y + Camera.BOUNDS.height / 2 > self.ocean_depth:
            self.direction = -1
            self.default_move_speed = 100

        self.__bounds_collision()

        for e in entities:
            if isinstance(e, OceanWall):
                if self.direction == -1:
                    e.set_direction(-1)
            elif isinstance(e, Fishy) and not e.captured:
                if self.bounds.colliderect(e.bounds):
                    e.hook_fish()
                    self.total_hooked_fish += 1
                    self.direction = -1

    def _move(self, direction=Direction.NONE):
        self.facing = direction
        if self.facing == Direction.LEFT:
            self.set_location(self.x - self.move_speed, self.y)
            self.velocity.x = -1
        if self.facing == Direction.RIGHT:
            self.set_location(self.x + self.move_speed, self.y)
            self.velocity.x = 1

    def _update_input(self, delta_time):
        self.input.update(delta_time)
        if self.input.pressing(InputType.LEFT):
            self._move(Direction.LEFT)
        if self.input.pressing(InputType.RIGHT):
            self._move(Direction.RIGHT)

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        self._update_input(delta_time)
        self._collision(entities)
        self.set_location(self.x, self.y + self.move_speed * self.direction)

    def draw(self, surface):        
        draw_line(
            surface,
            Camera.BOUNDS.width / 2 - 8, -8,
            self.x + 7, self.y - 6,
            CameraType.DYNAMIC,
            Color.BLACK,
            3
        )
        draw_line(
            surface,
            Camera.BOUNDS.width / 2 - 8, -8,
            self.x + 7, self.y - 6,
            CameraType.DYNAMIC,
            Color.WHITE,
            1
        )
        self.sprite.draw(surface, CameraType.DYNAMIC)

        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)


class OceanWall(Entity):
    def __init__(self, y, left, layer, total_layers):
        super(OceanWall, self).__init__(0 + layer *
                                        20 if left else Camera.BOUNDS.width - 32 - layer * 20, y, 32, 64)
        self.layer = layer
        self.sprite = Sprite(
            self.x, self.y, SpriteType.ROCK_WALL_L if left else SpriteType.ROCK_WALL_R)

        self.direction = 1
        self.parallax_layers = total_layers
        self.parallax_variance = 10
        self.parallax_speed = 0
        self.calculate_parallax_speed()

    def set_location(self, x, y):
        super(OceanWall, self).set_location(x, y)
        self.sprite.set_location(self.x, self.y)

    def set_direction(self, direction):
        self.direction = direction
        self.calculate_parallax_speed()

    def calculate_parallax_speed(self):
        assert (self.parallax_variance > 0), \
            "Parallax Variance must be greater than zero!"
        self.parallax_speed = self.parallax_variance * \
            (self.parallax_layers - (self.layer + 1))**2 * self.direction * -1

    def update_parallax(self, delta_time):
        self.set_location(self.x, self.y + self.parallax_speed * delta_time)

    def update(self, delta_time, entities):
        self.update_parallax(delta_time)

    def draw(self, surface):
        self.sprite.draw(surface, CameraType.DYNAMIC)


class Fishy(Kinetic):
    def __init__(self, y, left):
        super(Fishy, self).__init__(-32 if left else Camera.BOUNDS.width +
                                    16, y, 16, 16, randint(1, 10) * 10)
        self.type = randint(0, 1)
        self.velocity.x = -1 if left else 1
        if self.velocity.x > 0:
            if self.type == 0:
                self.sprite = Sprite(
                    self.x, self.y, SpriteType.FISH_SMALL_L if left else SpriteType.FISH_SMALL_R)
            elif self.type == 1:
                self.sprite = Sprite(
                    self.x, self.y, SpriteType.FISH_LARGE_L if left else SpriteType.FISH_LARGE_R)
        else:
            if self.type == 0:
                self.sprite = Sprite(
                    self.x, self.y, SpriteType.FISH_SMALL_L if left else SpriteType.FISH_SMALL_L)
            elif self.type == 1:
                self.sprite = Sprite(
                    self.x, self.y, SpriteType.FISH_LARGE_L if left else SpriteType.FISH_LARGE_L)

        self.captured = False

    def set_location(self, x, y):
        super(Fishy, self).set_location(x, y)
        self.sprite.set_location(self.x, self.y)

    def hook_fish(self):
        self.captured = True

    def _update_ai(self):
        self.set_location(self.x + self.move_speed * self.velocity.x, self.y)

    def flip_velocity(self):
        self.velocity.x *= -1
        if self.velocity.x > 0:
            if self.type == 0:
                self.sprite.set_sprite(SpriteType.FISH_SMALL_R)
            elif self.type == 1:
                self.sprite.set_sprite(SpriteType.FISH_LARGE_R)
        else:
            if self.type == 0:
                self.sprite.set_sprite(SpriteType.FISH_SMALL_L)
            elif self.type == 1:
                self.sprite.set_sprite(SpriteType.FISH_LARGE_L)

    def _collision(self, entities):
        if self.captured:
            for e in entities:
                if isinstance(e, Hook):
                    if self.velocity.x > 0:
                        self.set_location(
                            e.x - 6 + randint(-3, 3), e.y + 4 + randint(-3, 3))
                    else:
                        self.set_location(
                            e.x + 2 + randint(-3, 3), e.y + 4 + randint(-3, 3))

                    if randint(1, 10) <= 1:
                        self.flip_velocity()
                    return

        if (self.bounds.left < -32 and self.velocity.x < 0) or (self.bounds.right > Camera.BOUNDS.width + 32 and self.velocity.x > 0):
            self.flip_velocity()

    def update(self, delta_time, entities):
        self._calculate_scaled_speed(delta_time)
        # self._update_collision_rectangles()
        self._update_ai()
        self._collision(entities)

    def draw(self, surface):
        if pygine.globals.debug:
            self._draw_bounds(surface, CameraType.DYNAMIC)
            self._draw_collision_rectangles(surface)
        else:
            self.sprite.draw(surface, CameraType.DYNAMIC)
