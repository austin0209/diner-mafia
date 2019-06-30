import pygame
from pygame.mixer import Sound, music
from pygine import globals

pygame.mixer.init()

MUSIC_PATH = ""
SOUND_PATH = ""
if globals.on_cpi:
    MUSIC_PATH = '/home/cpi/games/Python/village-game/pygine/assets/music/'
    SOUND_PATH = '/home/cpi/games/Python/village-game/pygine/assets/sounds/'
else:
    MUSIC_PATH = 'pygine/assets/music/'
    SOUND_PATH = 'pygine/assets/sounds/'


def play_song(filename):
    music.load(MUSIC_PATH + filename)
    music.play(-1)


def play_sound(filename):
    Sound(SOUND_PATH + filename).play()
