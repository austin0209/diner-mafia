import pygame
import pygine.globals
from pygine.scenes import *
from pygine.utilities import Color, Input, InputType, StaticCamera
from enum import Enum


class GameState(Enum):
    QUIT = 0
    RUNNING = 1


class Orientaion(Enum):
    LANDSCAPE = 0
    PORTRAIT = 1


class Game:
    "A modest game engine used to streamline the development of a game made using pygame"
    state = GameState.QUIT

    def __init__(self):
        self.initialize_pygame()

        self.setup_window(320, 240, 60, False,
                          Orientaion.LANDSCAPE, "Village Game")
        self.setup_pixel_scene(320, 180)
        self.setup_cameras()

        Game.state = GameState.RUNNING
        self.delta_time = 0
        self.ticks = 0
        self.scene_manager = SceneManager()
        self.init_scenes()
        self.scene_manager.change_scene(SceneType.FOREST)
        self.input = Input()

    def init_scenes(self):
        self.scene_manager.add_scene(Village())
        self.scene_manager.add_scene(Forest())
        
    def initialize_pygame(self):
        pygame.init()

    def setup_window(self, window_width=1280, window_height=720, target_fps=60, fullscreen=False, orientation=Orientaion.LANDSCAPE, title="Game"):
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

    def setup_pixel_scene(self, game_width=320, game_height=180):
        self.game_width = game_width
        self.game_height = game_height

    def setup_cameras(self):
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

    def quit_game(self):
        Game.state = GameState.QUIT

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.window = pygame.display.set_mode(
                (self.display_width, self.display_height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height))

        self.setup_cameras()

    def calculate_delta_time(self):
        pygame.time.Clock().tick(self.target_fps)
        self.delta_time = (pygame.time.get_ticks() - self.ticks) / 1000.0
        self.ticks = pygame.time.get_ticks()

    def update_input(self):
        self.input.update()
        if self.input.pressing(InputType.QUIT):
            self.quit_game()
        if self.input.pressing(InputType.TOGGLE_FULLSCREEN):
            self.toggle_fullscreen()
        if self.input.pressing(InputType.TOGGLE_DEBUG):
            pygine.globals.debug = not pygine.globals.debug

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

    def clear_screen(self, color=Color.BLACK):
        "Clear the screen in preparation for the next draw call."
        self.window.fill(color)

    def update(self):
        self.calculate_delta_time()
        self.update_input()
        self.scene_manager.update(self.delta_time)
        self.update_events()

    def draw(self):
        if Game.state == GameState.QUIT:
            self.clear_screen(Color.BLACK)
        else:
            self.clear_screen(Color.SKY_BLUE)
            self.scene_manager.draw(self.window)

        self.static_camera.draw(self.window)
        pygame.display.update()

    def run(self):
        while Game.state != GameState.QUIT:
            self.update()
            self.draw()
        pygame.quit()
