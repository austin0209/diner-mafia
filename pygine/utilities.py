import pygame
from enum import IntEnum
from pygine.maths import Vector2


class Color:
    "A convenient list of RGB colors."
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    SKY_BLUE = (41, 173, 255)


class Timer:
    def __init__(self, length, started=False):
        self.length = length
        self.reset()
        self.started = started

    def start(self):
        self.started = True
        self.starting_ticks = pygame.time.get_ticks()

    def reset(self):
        self.started = False
        self.done = False
        self.starting_ticks = 0
        self.ticks = 0

    def update(self):
        if self.started and not self.done:
            self.ticks = pygame.time.get_ticks()
            if self.ticks - self.starting_ticks >= self.length:
                self.done = True


class InputType(IntEnum):
    NONE = 0

    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    A = 5
    B = 6
    X = 7
    Y = 8
    START = 9
    SELECT = 10

    RESET = 11
    TOGGLE_FULLSCREEN = 12
    TOGGLE_DEBUG = 13
    QUIT = 14


class Input:
    def __init__(self):
        self.key_state = None
        self.timer = Timer(200)
        self.no_spam = True

    def pressing(self, type):
        if type == InputType.UP:
            return self.key_state[pygame.K_UP] or self.key_state[pygame.K_w]
        if type == InputType.LEFT:
            return self.key_state[pygame.K_LEFT] or self.key_state[pygame.K_a]
        if type == InputType.DOWN:
            return self.key_state[pygame.K_DOWN] or self.key_state[pygame.K_s]
        if type == InputType.RIGHT:
            return self.key_state[pygame.K_RIGHT] or self.key_state[pygame.K_d]
        if type == InputType.A:
            return self.key_state[pygame.K_j]
        if type == InputType.B:
            return self.key_state[pygame.K_k]
        if type == InputType.X:
            return self.key_state[pygame.K_u]
        if type == InputType.Y:
            return self.key_state[pygame.K_i]
        if type == InputType.SELECT:
            return self.key_state[pygame.K_SPACE]
        if type == InputType.START:
            return self.key_state[pygame.K_KP_ENTER]

        if type == InputType.RESET:
            if self.key_state[pygame.K_r] and self.no_spam:
                self.no_spam = False
                self.timer.start()
                return True
        if type == InputType.TOGGLE_FULLSCREEN:
            if self.key_state[pygame.K_F10] and self.no_spam:
                self.no_spam = False
                self.timer.start()
                return True
        if type == InputType.TOGGLE_DEBUG:
            if self.key_state[pygame.K_F12] and self.no_spam:
                self.no_spam = False
                self.timer.start()
                return True

        if type == InputType.QUIT:
            return self.key_state[pygame.K_ESCAPE] or self.key_state[pygame.K_BACKSPACE]

        return False

    def update(self):
        self.key_state = pygame.key.get_pressed()
        self.timer.update()
        if not self.no_spam and self.timer.done:
            self.no_spam = True
            self.timer.reset()


class CameraType(IntEnum):
    DYNAMIC = 0
    STATIC = 1


class StaticCamera:
    BOUNDS = pygame.Rect(0, 0, 0, 0)
    scale = 0
    horizontal_letterbox = 0
    vertical_letterbox = 0
    top_left = Vector2()
    letterboxes = []

    def __init__(self, dimensions, scale):
        StaticCamera.horizontal_letterbox = 0
        StaticCamera.vertical_letterbox = 0
        StaticCamera.top_left = Vector2(
            -StaticCamera.horizontal_letterbox, - StaticCamera.vertical_letterbox)
        StaticCamera.scale = scale
        StaticCamera.BOUNDS = pygame.Rect(
            0, 0, dimensions[0], dimensions[1])

    def apply_horizontal_letterbox(self, horizontal_letterbox):
        StaticCamera.horizontal_letterbox = horizontal_letterbox
        StaticCamera.top_left.x = -StaticCamera.horizontal_letterbox

    def apply_vertical_letterbox(self, vertical_letterbox):
        StaticCamera.vertical_letterbox = vertical_letterbox
        StaticCamera.top_left.y = -StaticCamera.vertical_letterbox

    def draw(self, surface):
        # Top
        pygame.draw.rect(
            surface,
            Color.BLACK,
            (
                -32 * StaticCamera.scale,
                -32 * StaticCamera.scale,
                StaticCamera.BOUNDS.width * StaticCamera.scale + 64 * StaticCamera.scale,
                StaticCamera.vertical_letterbox + 32 * StaticCamera.scale
            )
        )

        # Bottom
        pygame.draw.rect(
            surface,
            Color.BLACK,
            (
                -32 * StaticCamera.scale,
                StaticCamera.vertical_letterbox +
                StaticCamera.BOUNDS.height * StaticCamera.scale,
                StaticCamera.BOUNDS.width * StaticCamera.scale + 64 * StaticCamera.scale,
                StaticCamera.vertical_letterbox + 32 * StaticCamera.scale
            )
        )

        # Left
        pygame.draw.rect(
            surface,
            Color.BLACK,
            (
                -32 * StaticCamera.scale,
                -32 * StaticCamera.scale,
                StaticCamera.horizontal_letterbox + 32 * StaticCamera.scale,
                StaticCamera.BOUNDS.height * StaticCamera.scale + 64 * StaticCamera.scale
            )
        )

        # Right
        pygame.draw.rect(
            surface,
            Color.BLACK,
            (
                StaticCamera.horizontal_letterbox +
                StaticCamera.BOUNDS.width * StaticCamera.scale + 1,
                -32 * StaticCamera.scale,
                StaticCamera.horizontal_letterbox,
                StaticCamera.BOUNDS.height * StaticCamera.scale + 64 * StaticCamera.scale
            )
        )


class Camera:
    BOUNDS = pygame.Rect(0, 0, 0, 0)
    scale = 0
    top_left = Vector2()

    def __init__(self, top_left=Vector2(0, 0)):
        Camera.scale = StaticCamera.scale
        Camera.top_left.x = top_left.x - StaticCamera.horizontal_letterbox
        Camera.top_left.y = top_left.y - StaticCamera.vertical_letterbox
        Camera.BOUNDS = pygame.Rect(
            Camera.top_left.x, Camera.top_left.y, StaticCamera.BOUNDS.width, StaticCamera.BOUNDS.height)

    def stay_within_bounds(self, top_left, world_bounds):
        if world_bounds.width == 0 or world_bounds.height == 0:
            world_bounds = pygame.Rect(
                0, 0, Camera.BOUNDS.width, Camera.BOUNDS.height)

        if top_left.x < world_bounds.left:
            top_left.x = world_bounds.left
        if top_left.x + Camera.BOUNDS.width > world_bounds.right:
            top_left.x = world_bounds.right - Camera.BOUNDS.width
        if top_left.y < world_bounds.top:
            top_left.y = world_bounds.top
        if top_left.y + Camera.BOUNDS.height > world_bounds.bottom:
            top_left.y = world_bounds.bottom - Camera.BOUNDS.height

        Camera.top_left.x = top_left.x * Camera.scale - StaticCamera.horizontal_letterbox
        Camera.top_left.y = top_left.y * Camera.scale - StaticCamera.vertical_letterbox

    def update(self, top_left=Vector2(0, 0), world_bounds=pygame.Rect(0, 0, 0, 0)):
        Camera.scale = StaticCamera.scale
        self.stay_within_bounds(top_left, world_bounds)
