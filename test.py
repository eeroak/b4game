import pygame as pg
import pygame_menu
import sys
import ctypes
from pygame_menu import sound
from pygame.locals import *
from pygame import mixer
pg.init()

mixer.init()
vol = mixer.music.set_volume(1)
print(vol)