import pygame
import pygine.globals
from pygine.scenes import *
from pygine.utilities import Color, Input, InputType, StaticCamera
from enum import IntEnum


class GameState(IntEnum):
    QUIT = 0
    RUNNING = 1


class Orientaion(IntEnum):
    LANDSCAPE = 0
    PORTRAIT = 1


class Game:
    "A modest game engine used to streamline the development of a game made using pygame"
    state = GameState.QUIT

    def __init__(self):
        self.__initialize_pygame()

        self.__setup_window(320, 240, 30, False,
                          Orientaion.LANDSCAPE, "Village Game")
        self.__setup_pixel_scene(320, 180)
        self.__setup_cameras()

        Game.state = GameState.RUNNING
        self.delta_time = 0
        self.ticks = 0
        self.scene_manager = SceneManager()
        self.input = Input()

    def __initialize_pygame(self):
        pygame.init()

    def __setup_window(self, window_width=1280, window_height=720, target_fps=60, fullscreen=False, orientation=Orientaion.LANDSCAPE, title="Game"):
        self.display_width = pygame.display.Info().current_w
        self.display_height = pygame.display.Info().current_h
        self.window_width = window_width
        self.window_height = window_height
        self.target_fps = target_fps
        self.orientation = orientation
        self.fullscreen = fullscreen

        if self.fullscreen:
            self.window = pygame.display.set_mode(
                (self.display_width, self.display_height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height))

        pygame.display.set_caption(title)

    def __setup_pixel_scene(self, game_width=320, game_height=180):
        self.game_width = game_width
        self.game_height = game_height

    def __setup_cameras(self):
        if self.orientation == Orientaion.LANDSCAPE:
            if self.fullscreen:
                self.scale = self.display_height / self.game_height
                if self.game_width * self.scale > self.display_width:
                    self.scale = self.display_width / self.game_width
            else:
                self.scale = self.window_height / self.game_height
                if self.game_width * self.scale > self.window_width:
                    self.scale = self.window_width / self.game_width

        elif self.orientation == Orientaion.PORTRAIT:
            if self.fullscreen:
                self.scale = self.display_width / self.game_width
                if self.game_height * self.scale > self.display_height:
                    self.scale = self.display_height / self.game_height
            else:
                self.scale = self.window_width / self.game_width
                if self.game_height * self.scale > self.window_height:
                    self.scale = self.window_height / self.game_height

        self.static_camera = StaticCamera(
            (self.game_width, self.game_height), self.scale)

        if self.fullscreen:
            if self.game_width * self.scale < self.display_width:
                self.static_camera.apply_horizontal_letterbox(
                    (self.display_width - self.game_width * self.scale) / 2)
            if self.game_height * self.scale < self.display_height:
                self.static_camera.apply_vertical_letterbox(
                    (self.display_height - self.game_height * self.scale) / 2)
        else:
            if self.game_width * self.scale < self.window_width:
                self.static_camera.apply_horizontal_letterbox(
                    (self.window_width - self.game_width * self.scale) / 2)
            if self.game_height * self.scale < self.window_height:
                self.static_camera.apply_vertical_letterbox(
                    (self.window_height - self.game_height * self.scale) / 2)

    def __quit_game(self):
        Game.state = GameState.QUIT

    def __toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.window = pygame.display.set_mode(
                (self.display_width, self.display_height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height))

        self.__setup_cameras()

    def __calculate_delta_time(self):
        pygame.time.Clock().tick(self.target_fps)
        self.delta_time = (pygame.time.get_ticks() - self.ticks) / 1000.0
        self.ticks = pygame.time.get_ticks()

    def __update_input(self, delta_time):
        self.input.update(delta_time)
        if self.input.pressing(InputType.QUIT):
            self.__quit_game()
        if self.input.pressing(InputType.TOGGLE_FULLSCREEN):
            self.__toggle_fullscreen()
        if self.input.pressing(InputType.TOGGLE_DEBUG):
            pygine.globals.debug = not pygine.globals.debug

    def __update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit_game()

    def __clear_screen(self, color=Color.BLACK):
        "Clear the screen in preparation for the next draw call."
        self.window.fill(color)

    def __update(self):
        self.__calculate_delta_time()
        self.__update_input(self.delta_time)
        self.scene_manager.update(self.delta_time)
        self.__update_events()

    def __draw(self):
        if Game.state == GameState.QUIT:
            self.__clear_screen(Color.BLACK)
        else:
            self.__clear_screen(Color.BLACK)
            self.scene_manager.draw(self.window)

        self.static_camera.draw(self.window)
        pygame.display.update()

    def run(self):
        while Game.state != GameState.QUIT:
            self.__update()
            self.__draw()
        pygame.quit()
