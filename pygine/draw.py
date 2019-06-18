import pygame
from pygine.math import Vector2
from pygine.utilities import Camera, Color, CameraType, StaticCamera


def __scaled_location(x, y, camera_type):
    if camera_type == CameraType.DYNAMIC:
        return Vector2(x * Camera.scale - Camera.top_left.x, y * Camera.scale - Camera.top_left.y)
    if camera_type == CameraType.STATIC:
        return Vector2(x * StaticCamera.scale - StaticCamera.top_left.x, y * StaticCamera.scale - StaticCamera.top_left.y)


def __scaled_value(value):
    return value * Camera.scale


def draw_rectangle(surface, rect, camera_type, color=Color.WHITE):
    pygame.draw.rect(
        surface,
        color,
        (
            __scaled_location(rect.x, rect.y, camera_type).x,
            __scaled_location(rect.x, rect.y, camera_type).y,
            __scaled_value(rect.width),
            __scaled_value(rect.height)
        )
    )


def draw_circle(surface, center, radius, camera_type, color=Color.WHITE, thickness=0):
    pygame.draw.circle(
        surface,
        color,
        (
            int(__scaled_location(center.x, center.y, camera_type).x),
            int(__scaled_location(center.x, center.y, camera_type).y),
        ),
        int(__scaled_value(radius)),
        int(__scaled_value(thickness))
    )


def draw_image(surface, image, rect, camera_type):
    image = pygame.transform.scale(
        image,
        (
            int(__scaled_value(rect.width)),
            int(__scaled_value(rect.height))
        )
    )
    surface.blit(
        image,
        (
            __scaled_location(rect.x, rect.y, camera_type).x,
            __scaled_location(rect.x, rect.y, camera_type).y
        )
    )
