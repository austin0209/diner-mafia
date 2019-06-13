import pygame
from utilities.vector import Vector2
from utilities.color import Color


class StaticCamera:
    SCALE = 0
    HORIZONTAL_LETTERBOX = 0
    VERTICAL_LETTERBOX = 0
    BOUNDS = pygame.Rect(0, 0, 0, 0)

    def __init__(self, dimensions=(0, 0), scale=1):
        StaticCamera.HORIZONTAL_LETTERBOX = 0
        StaticCamera.VERTICAL_LETTERBOX = 0
        StaticCamera.SCALE = scale
        StaticCamera.BOUNDS = pygame.Rect(
            0, 0, dimensions[0] * scale, dimensions[1] * scale)

    def apply_horizontal_letterbox(self, horizontal_letterbox=0):
        StaticCamera.HORIZONTAL_LETTERBOX = horizontal_letterbox

    def apply_vertical_letterbox(self, vertical_letterbox=0):
        StaticCamera.VERTICAL_LETTERBOX = vertical_letterbox

    def draw(self, surface):
        pygame.draw.rect(surface, Color.BLACK, (-32, -32,
                                                StaticCamera.BOUNDS.width + 64, StaticCamera.VERTICAL_LETTERBOX + 32))
        pygame.draw.rect(surface, Color.BLACK, (-32, StaticCamera.VERTICAL_LETTERBOX +
                                                StaticCamera.BOUNDS.height, StaticCamera.BOUNDS.width + 64, StaticCamera.VERTICAL_LETTERBOX + 32))
        pygame.draw.rect(surface, Color.BLACK, (-32, -32,
                                                StaticCamera.HORIZONTAL_LETTERBOX + 32, StaticCamera.BOUNDS.height + 64))
        pygame.draw.rect(surface, Color.BLACK, (StaticCamera.HORIZONTAL_LETTERBOX +
                                                StaticCamera.BOUNDS.width, -32, StaticCamera.HORIZONTAL_LETTERBOX, StaticCamera.BOUNDS.height + 64))


class Camera:
    SCALE = 0
    TOP_LEFT = Vector2()
    BOUNDS = pygame.Rect(0, 0, 0, 0)

    def __init__(self, top_left=Vector2(0, 0)):
        Camera.SCALE = StaticCamera.SCALE
        Camera.TOP_LEFT.x = top_left.x - StaticCamera.HORIZONTAL_LETTERBOX
        Camera.TOP_LEFT.y = top_left.y - StaticCamera.VERTICAL_LETTERBOX
        Camera.BOUNDS = pygame.Rect(
            Camera.TOP_LEFT.x, Camera.TOP_LEFT.y, StaticCamera.BOUNDS.width, StaticCamera.BOUNDS.height)

    def update(self, top_left=Vector2(0, 0)):
        Camera.SCALE = StaticCamera.SCALE
        Camera.TOP_LEFT.x = top_left.x * Camera.SCALE - StaticCamera.HORIZONTAL_LETTERBOX
        Camera.TOP_LEFT.y = top_left.y * Camera.SCALE - StaticCamera.VERTICAL_LETTERBOX
        Camera.BOUNDS.x = Camera.TOP_LEFT.x
        Camera.BOUNDS.y = Camera.TOP_LEFT.y
