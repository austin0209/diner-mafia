# TODO: Add the following: ButtonTrigger, TimedTrigger, MenuTrigger
# TODO BIG: Make NPC kinetic, make it so Collision and Button triggers only work for kinetic!
from enum import IntEnum
from pygine.base import PygineObject
from pygine.draw import draw_rectangle
from pygine.entities import Actor, Direction, Player, NPC
from pygine.utilities import InputType


class Trigger(PygineObject):
    def __init__(self, x, y, width, height, end_location, next_scene):
        super(Trigger, self).__init__(x, y, width, height)
        self.next_scene = next_scene
        self.end_location = end_location

    def _move_entity_to_next_scene(self, entity, manager):
        next_scene = manager.get_scene(self.next_scene)
        current_scene = manager.get_current_scene()
    
        if isinstance(entity, Player):
            manager.queue_next_scene(self.next_scene)
            next_scene.relay_player(entity)
        else:
            next_scene.relay_entity(entity)

        current_scene.entities.remove(entity)
        entity.set_location(self.end_location.x, self.end_location.y)

    def _valid_entity(self, entity):
        return isinstance(entity, Player) or isinstance(entity, NPC)

    def update(self, delta_time, entities, manager):
        raise NotImplementedError(
            "A class that inherits Trigger did not implement the update(delta_time, entities) method")

    def draw(self, surface, camera_type):
        raise NotImplementedError(
            "A class that inherits Trigger did not implement the draw(surface, camera_type) method")


class CollisionTrigger(Trigger):
    def __init__(self, x, y, width, height, end_location, next_scene, direction=Direction.UP):
        super(CollisionTrigger, self).__init__(
            x, y, width, height, end_location, next_scene)
        self.direction = direction

    def __collision(self, entities, manager):
        for e in entities:
            if self._valid_entity(e) and e.bounds.colliderect(self.bounds):
                self._move_entity_to_next_scene(e, manager)

    def update(self, delta_time, entities, manager):
        self.__collision(entities, manager)

    def draw(self, surface, camera_type):
        draw_rectangle(
            surface,
            self.bounds,
            camera_type
        )


class MinigameTrigger(Trigger):
    def __init__(self, x, y, width, height, end_location, next_scene, direction=Direction.UP):
        super(MinigameTrigger, self).__init__(
            x, y, width, height, end_location, next_scene)
        self.direction = direction

    def _move_entity_to_next_scene(self, entity, manager):
        assert (isinstance(entity, Actor)), "Should only relay actors!"
        current_scene = manager.get_current_scene()
        manager.queue_next_scene(self.next_scene)
        current_scene.entities.remove(entity)

    def __collision(self, entities, manager):
        for e in entities:
            if self._valid_entity(e) and e.bounds.colliderect(self.bounds):
                self._move_entity_to_next_scene(e, manager)

    def update(self, delta_time, entities, manager):
        self.__collision(entities, manager)

    def draw(self, surface, camera_type):
        draw_rectangle(
            surface,
            self.bounds,
            camera_type
        )


class ButtonTrigger(Trigger):
    def __init__(self, x, y, width, height, end_location, next_scene, direction=Direction.UP):
        super(ButtonTrigger, self).__init__(
            x, y, width, height, end_location, next_scene)
        self.direction = direction

    def __collision(self, entities, manager):
        for e in entities:
            if self._valid_entity(e) and e.bounds.colliderect(self.bounds):
                if isinstance(e, Player):
                    if e.input.pressing(InputType.A) and int(e.facing) == int(self.direction):
                        self._move_entity_to_next_scene(e, manager)
                elif isinstance(e, NPC):
                    self._move_entity_to_next_scene(e, manager)

    def update(self, delta_time, entities, manager):
        self.__collision(entities, manager)

    def draw(self, surface, camera_type):
        draw_rectangle(
            surface,
            self.bounds,
            camera_type
        )
