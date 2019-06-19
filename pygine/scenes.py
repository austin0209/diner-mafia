from pygame import Rect
from pygine.entities import *
from pygine.maths import Vector2
from pygine.transitions import Pinhole, PinholeType
from pygine.triggers import *
from pygine.utilities import Camera, Input, InputType
from enum import IntEnum


class SceneType(IntEnum):
    VILLAGE = 0
    FOREST = 1


class Scene(object):
    def __init__(self):
        self.camera = Camera()
        self.camera_location = Vector2(0, 0)
        self.bounds = Rect(0, 0, Camera.BOUNDS.width, Camera.BOUNDS.height)
        self.entities = []
        self.triggers = []
        self.input = Input()
        self.transition = None
        self.manager = None
        self.player = None

    def reset(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the reset() method")

    def create_triggers(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the create_triggers() method")

    def relay_player(self, player):
        self.player = player
        self.entities.append(self.player)

    def update_transition(self, delta_time):
        self.transition.update(delta_time)

    def update_input(self):
        self.input.update()
        if self.input.pressing(InputType.RESET):
            self.reset()

    def update_entities(self, delta_time):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the update_entities(delta_time) method")

    def update_triggers(self, delta_time, entities, manager):
        for t in self.triggers:
            t.update(delta_time, entities, manager)

    def update_camera(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the update_camera() method")

    def update(self, delta_time):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the update(delta_time) method")

    def draw(self, surface):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the draw(surface) method")


class SceneManager:
    def __init__(self):
        self.initialize_scenes()
        self.change_scene(SceneType.VILLAGE)
        self.__current_scene.relay_player(
            Player(
                Camera.BOUNDS.width / 2 - 3,
                Camera.BOUNDS.height / 2 - 8
            )
        )

    def initialize_scenes(self):
        self.__all_scenes = []
        self.add_scene(Village())
        self.add_scene(Forest())

    def set_current_scene(self, scene_type):
        self.__current_scene = None

    def add_scene(self, scene):
        self.__all_scenes.append(scene)
        scene.manager = self

    def get_scene(self, scene_type):
        return self.__all_scenes[int(scene_type)]

    def get_current_scene(self):
        return self.__current_scene

    def change_scene(self, scene_type):
        assert len(self.__all_scenes) != 0
        if scene_type == SceneType.VILLAGE:
            self.__current_scene = self.__all_scenes[int(SceneType.VILLAGE)]
        elif scene_type == SceneType.FOREST:
            self.__current_scene = self.__all_scenes[int(SceneType.FOREST)]
        #self.__current_scene.reset()
        self.__current_scene.transition = Pinhole(PinholeType.OPEN)

    def update(self, delta_time):
        assert self.__current_scene != None
        self.__current_scene.update(delta_time)

    def draw(self, surface):
        assert self.__current_scene != None
        self.__current_scene.draw(surface)


class Village(Scene):
    def __init__(self):
        super(Village, self).__init__()
        self.create_triggers()
        self.reset()

    def create_triggers(self):
        self.triggers.append(CollisionTrigger(0, 0, 16, Camera.BOUNDS.height, Vector2(
            Camera.BOUNDS.width - 16 - 16, 0), SceneType.FOREST))

    def reset(self):
        self.player = None
        self.entities = [
            # self.player,
            SpecialHouse(16 + 48 * 1 + 16, 16),
            NPC(16 * 8, 16 * 6, NPCType.MALE),
            NPC(16 * 12, 16 * 3, NPCType.FEMALE),
            NPC(16 * 18, 16 * 9, NPCType.FEMALE),

            Tree(16 + 16 * 0, 16 + 16 * 0),
            Tree(32 + 16 * 0, 16 + 16 * 0),
            Tree(64 + 16 * 0, 16 + 16 * 0),
            Tree(32 + 16 * 0, 32 + 16 * 0),
            Tree(48 + 16 * 0, 48 + 16 * 0),

            Tree(16 + 16 * 2, 16 + 16 * 8),
            Tree(32 + 16 * 2, 16 + 16 * 8),
            Tree(64 + 16 * 2, 16 + 16 * 8),
            Tree(32 + 16 * 2, 32 + 16 * 8),
            Tree(48 + 16 * 2, 48 + 16 * 8),

            Tree(16 + 16 * 10, 16 + 16 * 6),
            Tree(32 + 16 * 10, 16 + 16 * 6),
            Tree(64 + 16 * 10, 16 + 16 * 6),
            Tree(32 + 16 * 10, 32 + 16 * 6),
            Tree(48 + 16 * 10, 48 + 16 * 6),

            Tree(16 + 16 * 15, 16 + 16 * 2),
            Tree(32 + 16 * 15, 16 + 16 * 2),
            Tree(64 + 16 * 15, 16 + 16 * 2),
            Tree(32 + 16 * 15, 32 + 16 * 2),
            Tree(48 + 16 * 15, 48 + 16 * 2),
        ]
        self.transition = Pinhole(PinholeType.OPEN)
        self.sprites = []
        for y in range(int(Camera.BOUNDS.height * 2 / 32)):
            for x in range(int(Camera.BOUNDS.width * 2 / 32)):
                self.sprites.append(Sprite(x * 32, y * 32, SpriteType.GRASS))

    def update_camera(self):
        self.camera_location = Vector2(
            self.player.x + self.player.width / 2 - self.camera.BOUNDS.width / 2,
            self.player.y + self.player.height / 2 - self.camera.BOUNDS.height / 2
        )
        self.camera.update(self.camera_location)

    def update_entities(self, delta_time):
        for i in range(len(self.entities)-1, -1, -1):
            self.entities[i].update(delta_time, self.entities)
        self.entities.sort(key=lambda e: e.y + e.height)

    def update(self, delta_time):
        self.update_transition(delta_time)
        self.update_input()
        self.update_entities(delta_time)
        self.update_triggers(delta_time, self.entities, self.manager)
        self.update_camera()

    def draw(self, surface):
        for s in self.sprites:
            s.draw(surface, CameraType.DYNAMIC)
        for e in self.entities:
            e.draw(surface)
        for t in self.triggers:
            t.draw(surface, CameraType.DYNAMIC)
        self.transition.draw(surface)


class Forest(Scene):
    def __init__(self):
        super(Forest, self).__init__()
        self.create_triggers()
        self.reset()

    def create_triggers(self):
        self.triggers.append(
            CollisionTrigger(
                Camera.BOUNDS.width - 16,
                0,
                16,
                Camera.BOUNDS.height,
                Vector2(16, 0),
                SceneType.VILLAGE
            )
        )

    def reset(self):

        self.entities = [
            # self.player,

            Tree(16 + 16 * 0, 16 + 16 * 0),
            Tree(32 + 16 * 0, 16 + 16 * 0),
            Tree(64 + 16 * 0, 16 + 16 * 0),
            Tree(32 + 16 * 0, 32 + 16 * 0),
            Tree(48 + 16 * 0, 48 + 16 * 0),

            Tree(16 + 16 * 2, 16 + 16 * 8),
            Tree(32 + 16 * 2, 16 + 16 * 8),
            Tree(64 + 16 * 2, 16 + 16 * 8),
            Tree(32 + 16 * 2, 32 + 16 * 8),
            Tree(48 + 16 * 2, 48 + 16 * 8),

            Tree(16 + 16 * 10, 16 + 16 * 6),
            Tree(32 + 16 * 10, 16 + 16 * 6),
            Tree(64 + 16 * 10, 16 + 16 * 6),
            Tree(32 + 16 * 10, 32 + 16 * 6),
            Tree(48 + 16 * 10, 48 + 16 * 6),

            Tree(16 + 16 * 15, 16 + 16 * 2),
            Tree(32 + 16 * 15, 16 + 16 * 2),
            Tree(64 + 16 * 15, 16 + 16 * 2),
            Tree(32 + 16 * 15, 32 + 16 * 2),
            Tree(48 + 16 * 15, 48 + 16 * 2),
        ]
        self.transition = Pinhole(PinholeType.OPEN)
        self.sprites = []
        for y in range(int(Camera.BOUNDS.height * 2 / 32)):
            for x in range(int(Camera.BOUNDS.width * 2 / 32)):
                self.sprites.append(Sprite(x * 32, y * 32, SpriteType.GRASS))

    def update_camera(self):
        self.camera_location = Vector2(
            self.player.x + self.player.width / 2 - self.camera.BOUNDS.width / 2,
            self.player.y + self.player.height / 2 - self.camera.BOUNDS.height / 2
        )
        self.camera.update(self.camera_location)

    def update_entities(self, delta_time):
        for i in range(len(self.entities)-1, -1, -1):
            self.entities[i].update(delta_time, self.entities)
        self.entities.sort(key=lambda e: e.y + e.height)

    def update(self, delta_time):
        self.update_transition(delta_time)
        self.update_input()
        self.update_entities(delta_time)
        self.update_triggers(delta_time, self.entities, self.manager)
        self.update_camera()

    def draw(self, surface):
        for s in self.sprites:
            s.draw(surface, CameraType.DYNAMIC)
        for e in self.entities:
            e.draw(surface)
        for t in self.triggers:
            t.draw(surface, CameraType.DYNAMIC)
        self.transition.draw(surface)
