from enum import IntEnum
from random import randint, random, seed
from pygame import Rect
from pygine.entities import *
from pygine.maths import Vector2
from pygine.transitions import Pinhole, TransitionType
from pygine.triggers import *
from pygine.utilities import Camera, Input, InputType


class SceneType(IntEnum):
    VILLAGE = 0
    FOREST = 1
    FARM = 2
    OCEAN = 3
    ROOM_SIMPLE = 4
    ROOM_SPECIAL = 5
    SHOP = 6
    DINER = 7
    COFFEE_MINIGAME = 8
    CROP_MINIGAME = 9
    FISH_MINIGAME = 10
    EGGS_MINIGAME = 11


class SceneManager:
    def __init__(self):
        self.input = Input()
        self.__reset()

    def get_scene(self, scene_type):
        return self.__all_scenes[int(scene_type)]

    def get_current_scene(self):
        return self.__current_scene

    def __reset(self):
        self.__all_scenes = []
        self.__current_scene = None
        self.__previous_scene = None
        self.__next_scene = None
        self.leave_transition = None
        self.enter_transition = None
        self.start_transition = False

        self.__initialize_scenes()
        self.__set_starting_scene(SceneType.VILLAGE)

    def __add_scene(self, scene):
        self.__all_scenes.append(scene)
        scene.manager = self

    def __initialize_scenes(self):
        # Scenes must be added in the same order as declared in the IntEnum
        self.__all_scenes = []
        self.__add_scene(Village())
        self.__add_scene(Forest())
        self.__add_scene(Farm())
        self.__add_scene(Ocean())
        self.__add_scene(RoomSimple())
        self.__add_scene(RoomSpecial())
        self.__add_scene(ShopScene())
        self.__add_scene(DinerScene())
        self.__add_scene(CoffeeMinigame())
        self.__add_scene(CropMinigame())
        self.__add_scene(FishMinigame())
        self.__add_scene(EggsMinigame())

    def __set_starting_scene(self, starting_scene_type):
        assert (len(self.__all_scenes) > 0), \
            "It looks like you never initialized all the scenes! Make sure to setup and call __initialize_scenes()"

        self.__current_scene = self.__all_scenes[int(starting_scene_type)]
        self.__current_scene.relay_player(
            Player(
                16 * 4,
                16 * 9
            )
        )

    def __setup_transition(self):
        if self.__previous_scene.leave_transition_type == TransitionType.PINHOLE_CLOSE:
            self.leave_transition = Pinhole(TransitionType.PINHOLE_CLOSE)

        if self.__next_scene.enter_transition_type == TransitionType.PINHOLE_OPEN:
            self.enter_transition = Pinhole(TransitionType.PINHOLE_OPEN)

        self.start_transition = True

    def queue_next_scene(self, scene_type, end_location):
        self.__end_location = end_location
        self.__previous_scene = self.__current_scene
        self.__next_scene = self.__all_scenes[int(scene_type)]
        self.__setup_transition()

    def __change_scenes(self):
        self.__current_scene.player.set_location(self.__end_location.x, self.__end_location.y)
        self.__current_scene = self.__next_scene

    def __update_input(self):
        self.input.update()
        if self.input.pressing(InputType.RESET):
            self.__reset()

    def __update_transition(self, delta_time):
        if self.start_transition and not self.enter_transition.done:
            self.leave_transition.update(delta_time)
            if self.leave_transition.done:
                self.enter_transition.update(delta_time)
                self.__change_scenes()
        else:
            self.start_transition = False

    def update(self, delta_time):
        assert (self.__current_scene != None), \
            "It looks like you never set a starting scene! Make sure to call __set_starting_scene(starting_scene_type)"

        self.__update_input()
        self.__update_transition(delta_time)
        if not self.start_transition:
            self.__current_scene.update(delta_time)

    def __draw_transitions(self, surface):
        if self.start_transition:
            if self.leave_transition != None and not self.leave_transition.done:
                self.leave_transition.draw(surface)
                if self.leave_transition.done:
                    self.enter_transition.draw(surface)
            else:
                self.enter_transition.draw(surface)

    def draw(self, surface):
        assert (self.__current_scene != None), \
            "It looks like you never set a starting scene! Make sure to call __set_starting_scene(starting_scene_type)"

        self.__current_scene.draw(surface)
        self.__draw_transitions(surface)


class Scene(object):
    def __init__(self):
        self.camera = Camera()
        self.camera_location = Vector2(0, 0)
        self.bounds = Rect(0, 0, Camera.BOUNDS.width, Camera.BOUNDS.height)
        self.sprites = []
        self.entities = []
        self.shapes = []
        self.triggers = []

        self.leave_transition_type = TransitionType.PINHOLE_CLOSE
        self.enter_transition_type = TransitionType.PINHOLE_OPEN

        # this is to be set in SceneManager (add scene method)
        self.manager = None
        self.player = None

    def _reset(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the reset() method")

    def _create_triggers(self):
        raise NotImplementedError(
            "A class that inherits Scene did not implement the create_triggers() method")

    def relay_player(self, player):
        self.player = player
        self.entities.append(self.player)

    def relay_entity(self, entity):
        self.entities.append(entity)
        # We can potentially add aditional logic for certain entites. For example, if the entity is a NPC then spawn it at (x, y)

    def __update_entities(self, delta_time):
        for i in range(len(self.entities) - 1, -1, -1):
            self.entities[i].update(delta_time, self.entities)
        self.entities.sort(key=lambda e: (e.sprite.y + e.sprite.height) * 10 - e.sprite.x)

    def __update_triggers(self, delta_time, entities, manager):
        for t in self.triggers:
            t.update(delta_time, entities, manager)

    def __update_camera(self):
        self.camera_location = Vector2(
            self.player.x + self.player.width / 2 - self.camera.BOUNDS.width / 2,
            self.player.y + self.player.height / 2 - self.camera.BOUNDS.height / 2
        )
        self.camera.update(self.camera_location, self.bounds)

    def update(self, delta_time):
        self.__update_entities(delta_time)
        self.__update_triggers(delta_time, self.entities, self.manager)
        self.__update_camera()

    def draw(self, surface):
        for s in self.shapes:
            s.draw(surface, CameraType.DYNAMIC)
        for s in self.sprites:
            s.draw(surface, CameraType.DYNAMIC)
        for e in self.entities:
            e.draw(surface)
        if pygine.globals.debug:
            for t in self.triggers:
                t.draw(surface, CameraType.DYNAMIC)


class Village(Scene):
    def __init__(self):
        super(Village, self).__init__()
        self._reset()
        self._create_triggers()
        self.__load_trees()

    def __load_trees(self):
        file = open('pygine/assets/scenes/trees.csv', "r")
        for y in range(20):
            row = file.readline().split(",")
            for x in range(40):
                column = row[x]
                if column.strip() != "-1" and randint(1, 10) <= 8:
                    self.entities.append(Tree(x * 16, y * 16))

    def _reset(self):
        self.bounds = Rect(0, 0, 40 * 16, 19 * 16)

        self.shapes = [Rectangle(0, 0, 320 * 2, 180 * 2, Color.GRASS_GREEN)]
        self.sprites = [
            Sprite(-1 * 16, 6 * 16, SpriteType.SIDEWALK_LONG),
            Sprite(2 * 16, 15 * 16, SpriteType.SIDEWALK_LONG),
            Sprite(18 * 16, 0 * 16, SpriteType.SIDEWALK_TALL),
        ]

        self.entities = [
            SimpleHouse(1 * 16, 1 * 16),
            SimpleHouse(9 * 16, 10 * 16),
            SimpleHouse(14 * 16, 10 * 16),
            SpecialHouse(5 * 16, 1 * 16),
            SpecialHouse(12 * 16, 1 * 16),
            SpecialHouse(2 * 16, 10 * 16),
            Shop(20 * 16, 0 * 16),
            Shop(25 * 16, 0 * 16),
            Shop(30 * 16, 0 * 16),
            Shop(35 * 16, 0 * 16),
            Diner(21 * 16, 10 * 16),

        ]

    def _create_triggers(self):
        self.triggers = [
            CollisionTrigger(
                -1 * 16, 6 * 16,
                16, 32,
                Vector2(
                    Camera.BOUNDS.width - 16 - 16, Camera.BOUNDS.height / 2
                ),
                SceneType.FOREST
            ),
            CollisionTrigger(
                18 * 16, -1 * 16,
                32, 16,
                Vector2(Camera.BOUNDS.width / 2, Camera.BOUNDS.height - 16),
                SceneType.OCEAN
            )
        ]

        for e in self.entities:
            if isinstance(e, Building):
                if isinstance(e, SimpleHouse):
                    self.triggers.append(
                        ButtonTrigger(
                            e.x + (40 - 16) / 2, e.y + 40,
                            16, 8,
                            Vector2(
                                9 * 16 + 8 + 3, 8 * 16 + 10
                            ),
                            SceneType.ROOM_SIMPLE
                        )
                    )
                if isinstance(e, SpecialHouse):
                    self.triggers.append(
                        ButtonTrigger(
                            e.x + (40 - 16) / 2, e.y + 40,
                            16, 8,
                            Vector2(
                                16 * 5 + 11, 16 * 8 + 10
                            ),
                            SceneType.ROOM_SPECIAL
                        )
                    )
                if isinstance(e, Shop):
                    self.triggers.append(
                        ButtonTrigger(
                            e.x, e.y + 32,
                            32, 8,
                            Vector2(
                                16 * 5 + 11, 16 * 8 + 10
                            ),
                            SceneType.SHOP
                        )
                    )
                if isinstance(e, Diner):
                    self.triggers.append(
                        ButtonTrigger(
                            e.x + 16, e.y + 32,
                            16, 8,
                            Vector2(
                                16 * 5 + 11, 16 * 8 + 10
                            ),
                            SceneType.DINER
                        )
                    )


class Forest(Scene):
    def __init__(self):
        super(Forest, self).__init__()
        self._reset()
        self._create_triggers()

    def _reset(self):
        self.shapes = []
        self.sprites = []
        for y in range(int(Camera.BOUNDS.height * 2 / 32)):
            for x in range(int(Camera.BOUNDS.width * 2 / 32)):
                self.sprites.append(Sprite(x * 32, y * 32, SpriteType.GRASS))

        self.entities = [
            Tree(16 + 16 * 0, 16 + 16 * 0),
            Tree(32 + 16 * 0, 16 + 16 * 0),
            Tree(64 + 16 * 0, 16 + 16 * 0),
            Tree(32 + 16 * 0, 32 + 16 * 0),
            Tree(48 + 16 * 0, 48 + 16 * 0),

            Tree(16 + 16 * 10, 16 + 16 * 5),
            Tree(32 + 16 * 10, 16 + 16 * 5),
            Tree(64 + 16 * 10, 16 + 16 * 5),
            Tree(32 + 16 * 10, 32 + 16 * 5),
            Tree(48 + 16 * 10, 48 + 16 * 5),

            Tree(16 + 16 * 7, 16 + 16 * 3),
            Tree(32 + 16 * 7, 16 + 16 * 3),
            Tree(64 + 16 * 7, 16 + 16 * 3),
            Tree(32 + 16 * 7, 32 + 16 * 3),
            Tree(48 + 16 * 7, 48 + 16 * 3),

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

    def _create_triggers(self):
        self.triggers.append(
            CollisionTrigger(
                Camera.BOUNDS.width - 8, 0,
                8, Camera.BOUNDS.height,
                Vector2(16, Camera.BOUNDS.height / 2),
                SceneType.VILLAGE
            )
        )


class Farm(Scene):
    def __init__(self):
        super(Farm, self).__init__()

    def _reset(self):
        pass


class Ocean(Scene):
    def __init__(self):
        super(Ocean, self).__init__()
        self._reset()
        self._create_triggers()

    def _reset(self):
        self.bounds = Rect(0, 0, 320, 180)

        self.shapes = [Rectangle(0, 0, 320, 180, Color.OCEAN_BLUE)]
        self.sprites = [
            Sprite(0, 0, SpriteType.BEACH),
        ]

        self.entities = [
        ]

    def _create_triggers(self):
        self.triggers = [
            MinigameTrigger(
                12 * 16, 2 * 16 + 4,
                32, 16,
                Vector2(
                    16, Camera.BOUNDS.height / 2
                ),
                SceneType.COFFEE_MINIGAME
            ),
            CollisionTrigger(
                0, Camera.BOUNDS.height, 
                Camera.BOUNDS.width, 16,
                Vector2(18 * 16, 1 * 16),
                SceneType.VILLAGE
            )
        ]


class RoomSimple(Scene):
    def __init__(self):
        super(RoomSimple, self).__init__()
        self._reset()
        self._create_triggers()

    def _reset(self):
        self.shapes = []
        self.sprites = [
            Sprite((Camera.BOUNDS.width - 160) / 2,
                   (Camera.BOUNDS.height - 160) / 2, SpriteType.SIMPLE_HOUSE_INSIDE)
        ]
        self.entities = [
            FlowerPot(7 * 16, 5 * 16),
            Shelf(8 * 16, 5 * 16),
            Bed(11 * 16, 5 * 16),
            Wall(6, 4, 8, 1),
            Wall(5, 5, 1, 4),
            Wall(6, 9, 3, 1),
            Wall(11, 9, 3, 1),
            Wall(14, 5, 1, 4),

        ]

    def _create_triggers(self):
        self.triggers.append(
            CollisionTrigger(
                9 * 16, 9 * 16 + 10,
                32, 16,
                Vector2(16 + 48 * 1 + 16 + 16, 16 + 64),
                SceneType.VILLAGE
            )
        )


class RoomSpecial(Scene):
    def __init__(self):
        super(RoomSpecial, self).__init__()
        self._reset()
        self._create_triggers()

    def _reset(self):
        self.shapes = []
        self.sprites = [
            Sprite((Camera.BOUNDS.width - 288) / 2,
                   (Camera.BOUNDS.height - 160) / 2, SpriteType.SPECIAL_HOUSE_INSIDE)
        ]
        self.entities = [
            Shelf(3 * 16, 5 * 16),
            FlowerPot(5 * 16, 5 * 16),
            Sofa(8 * 16, 6 * 16),
            Bed(13 * 16, 5 * 16),
            Bed(15 * 16, 5 * 16),

            Wall(2, 4, 16, 1),
            Wall(1, 5, 1, 4),
            Wall(2, 9, 3, 1),
            Wall(7, 9, 11, 1),
            Wall(18, 5, 1, 4),

        ]

    def _create_triggers(self):
        self.triggers.append(
            CollisionTrigger(
                5 * 16, 9 * 16 + 10,
                32, 16,
                Vector2(16 + 48 * 1 + 16 + 16, 16 + 64),
                SceneType.VILLAGE
            )
        )


class ShopScene(Scene):
    def __init__(self):
        super(ShopScene, self).__init__()
        self._reset()
        self._create_triggers()

    def _reset(self):
        self.shapes = []
        self.sprites = [
            Sprite((Camera.BOUNDS.width - 288) / 2,
                   (Camera.BOUNDS.height - 160) / 2, SpriteType.SHOP_INSIDE)
        ]
        self.entities = [
            CounterShop(2 * 16, 6 * 16),
            Shelf(10 * 16, 5 * 16, False),
            Shelf(12 * 16, 5 * 16, False),
            Shelf(14 * 16, 5 * 16),
            Shelf(16 * 16, 5 * 16, False),
            Shelf(14 * 16, 7 * 16, False),
            Shelf(16 * 16, 7 * 16),
            Wall(2, 4, 16, 1),
            Wall(1, 5, 1, 4),
            Wall(2, 9, 3, 1),
            Wall(7, 9, 11, 1),
            Wall(18, 5, 1, 4),

        ]

    def _create_triggers(self):
        self.triggers.append(
            CollisionTrigger(
                5 * 16, 9 * 16 + 10,
                32, 16,
                Vector2(16 + 48 * 1 + 16 + 16, 16 + 64),
                SceneType.VILLAGE
            )
        )


class DinerScene(Scene):
    def __init__(self):
        super(DinerScene, self).__init__()
        self._reset()
        self._create_triggers()

    def _reset(self):
        self.shapes = []
        self.sprites = [
            Sprite((Camera.BOUNDS.width - 288) / 2,
                   (Camera.BOUNDS.height - 160) / 2, SpriteType.DINER_INSIDE)
        ]
        self.entities = [
            CounterDiner(2 * 16, 5 * 16),
            StoolTall(2 * 16, 6 * 16),
            StoolTall(3 * 16, 6 * 16),
            StoolTall(4 * 16, 6 * 16),
            StoolTall(5 * 16, 6 * 16),
            StoolShort(12 * 16, 8 * 16),
            StoolShort(14 * 16, 7 * 16),
            Table(13 * 16, 8 * 16),
            Table(15 * 16, 8 * 16),
            Table(15 * 16, 7 * 16),
            Wall(2, 3, 16, 1),
            Wall(1, 4, 1, 5),
            Wall(2, 9, 3, 1),
            Wall(7, 9, 11, 1),
            Wall(18, 4, 1, 5),

        ]

    def _create_triggers(self):
        self.triggers.append(
            CollisionTrigger(
                5 * 16, 9 * 16 + 10,
                32, 16,
                Vector2(16 + 48 * 1 + 16 + 16, 16 + 64),
                SceneType.VILLAGE
            )
        )


class Minigame(Scene):
    def __init__(self):
        super(Minigame, self).__init__()

    def start_game(self):
        raise NotImplementedError(
            "A class that inherits Minigame did not implement the start_game() method")

    def _exit_game(self, end_x, end_y, item, new_scene):
        # TODO: should take you to dock scene later
        self.manager.queue_next_scene(new_scene, Vector2(end_x, end_y))
        new_player = Player(end_x, end_y)
        new_player.item_carrying = item
        self.manager.get_scene(new_scene).relay_player(new_player)


class CoffeeMinigame(Minigame):
    def __init__(self):
        super(CoffeeMinigame, self).__init__()
        self._reset()
        self._create_triggers()

    def start_game(self):
        self.__game_timer.start()

    def _reset(self):
        self.shapes = [
            Rectangle(0, 0, 320, 16 * 4, Color.BLUE),
            Rectangle(0, 16 * 4, 320, 16 * 6 + 20, Color.SKY_BLUE)
        ]
        self.sprites = []
        self.entities = []
        self.relay_player(
            Boat(
                16 * 4,
                16 * 9
            )
        )
        self.__game_timer = Timer(35000)
        self.__spawn_timer = Timer(1500, True)

    def _create_triggers(self):
        pass

    def __spawn_random(self):
        grid_unit_size = self.player.playbounds.height / 5
        rand_x = randint(-2, 4) * grid_unit_size + Camera.BOUNDS.width
        rand_y = randint(-2, 4) * grid_unit_size + self.player.playbounds.y
        if random() < 0.40:
            self.entities.append(Octopus(rand_x, rand_y))
        else:
            min_offset = 0
            max_offset = 30
            self.entities.append(Rock(rand_x, rand_y))
            for i in range(randint(0, 4)):
                self.entities.append(
                    Rock(rand_x + randint(min_offset, max_offset), rand_y + randint(min_offset, max_offset)))

    def update(self, delta_time):
        self.__game_timer.update()
        if self.__game_timer.done:
            # Game is over, change scene
            # TODO: should be dock later
            self._exit_game(12 * 16 + 11, 4 * 16, Coffee(0, 0), SceneType.OCEAN)
            self._reset()
            self.__game_timer.reset()
        else:
            self.__spawn_timer.update()
            if self.__spawn_timer.done:
                if randint(1,10) <= 7:
                    self.__spawn_random()
                self.__spawn_timer.reset()
                self.__spawn_timer.start()
            for e in self.entities:
                if e.sprite.x + e.sprite.width < 0:
                    self.entities.remove(e)
                if isinstance(e, Bullet):
                    if e.dead:
                        self.entities.remove(e)
            super(CoffeeMinigame, self).update(delta_time)

    def draw(self, surface):
        draw_rectangle(surface, self.player.playbounds,
                       CameraType.DYNAMIC, Color.SKY_BLUE)
        super(CoffeeMinigame, self).draw(surface)


class CropMinigame(Scene):
    def __init__(self):
        super(CropMinigame, self).__init__()

    def _reset(self):
        pass


class FishMinigame(Scene):
    def __init__(self):
        super(FishMinigame, self).__init__()

    def _reset(self):
        pass


class EggsMinigame(Scene):
    def __init__(self):
        super(EggsMinigame, self).__init__()

    def _reset(self):
        pass
