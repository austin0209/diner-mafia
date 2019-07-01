import pygame
from pygame.mixer import Sound, music
from pygine import globals

MUSIC_PATH = ""
SOUND_PATH = ""
current_song = ""


def load_sound_paths():
    global MUSIC_PATH
    global SOUND_PATH
    if globals.on_cpi:
        MUSIC_PATH = '/home/cpi/games/Python/diner-mafia/pygine/assets/music/'
        SOUND_PATH = '/home/cpi/games/Python/diner-mafia/pygine/assets/sounds/'
    else:
        MUSIC_PATH = 'pygine/assets/music/'
        SOUND_PATH = 'pygine/assets/sounds/'

    pygame.mixer.init()
    music.set_volume(0.80)


def play_song(filename):
    global current_song
    global MUSIC_PATH
    if filename != current_song:
        music.load(MUSIC_PATH + filename)
        music.play(-1)
        current_song = filename


def play_sound(filename):
    global SOUND_PATH
    Sound(SOUND_PATH + filename).play()
