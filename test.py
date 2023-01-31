import pygame as pg
import pygame_menu
import sys
import ctypes
from pygame_menu import sound
from pygame.locals import *
from pygame import mixer
pg.init()
user32 = ctypes.windll.user32
user32.SetProcessDPIAware(2)
width = 1920
lenght = 1080
dispSurf = pg.display.set_mode((width,lenght), vsync=1)


asetukset = pygame_menu.Menu('Asetukset', 1280, 720, center_content=True, 
                         mouse_enabled=True, theme=pygame_menu.themes.THEME_DARK, menu_id="2",)

asetukset.add.range_slider('Äänenvoimakkuus', 50, (0,100), 1, 
                           value_format=lambda x: str(int(x)),) #muokkaa sliderin näyttämään vain kokonaislukuja
asetukset.mainloop(dispSurf)