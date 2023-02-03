from time import sleep
import pygame as pg
import pygame_menu
import sys
import ctypes
from pygame_menu import sound
from pygame.locals import *
from pygame import mixer

pg.init()

#tekee näytön skaalauksesta mukautuvan jokaiselle resoluutiolle (alle full HD tuskin toimii kunnolla)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware(2)
width = 1920
lenght = 1080
dispSurf = pg.display.set_mode((width,lenght), vsync=1)
#dispFail = pg.display.set_mode((width,lenght), vsync=1)
pg.display.set_caption("Hissipeli")

# kaikki renderöitävät objektit
level = pg.image.load("Hissipeli_ovet_kiinni.jpg").convert()
player = pg.image.load("hissiukko ilo.png").convert()
ylakerta = pg.image.load("ylakerta.png").convert()
ylanappi = pg.image.load("ylanappi.png")
alakerta = pg.image.load("alakerta.png").convert()
alanappi = pg.image.load("alanappi.jpg").convert()
gover = pg.image.load("gameover.jpg").convert()

# pelaajan rajojen placeholderit
border_top = pg.Rect(30, 220, 325, 1)
border_btm = pg.Rect(30, 1015, 325, 1)

# otan hissien vieressä seisovien ukkelien kuvista taustat pois
ylakerta.set_colorkey((255,255,255))
ylanappi.set_colorkey((255,255,255))
alakerta.set_colorkey((255,255,255))
alanappi.set_colorkey((255,255,255))
player.set_colorkey((255,255,255))

dispSurf.blit(level, (0,0))
dispSurf.blit(player, (400,300))
dispSurf.blit(ylakerta,(200,300))
dispSurf.blit(ylanappi,(200,300))
dispSurf.blit(alakerta,(500,600))
dispSurf.blit(alanappi,(500,600))
dispSurf.blit(gover,(0,0))

pg.display.flip()

playerArea = player.get_rect()

#pelaajan hahmon aloituspaikan liikuttaminen (pikseleissä)
playerArea.left = 30
playerArea.top = 723

# pelin taustaäänet/valikkoäänet
""" mixer.init() 
mixer.music.load('Doom.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.5) """
sEngine = sound.Sound()
sEngine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION,('menuselect.ogg'))
sEngine.set_sound(sound.SOUND_TYPE_CLOSE_MENU,('menuselect.ogg'))

press_down = False
press_up = False

def failup():
    global press_up
    press_up=False

def failbtm():
    global press_down
    press_down = False

def game_over():
    print("game over")
    dispSurf.blit(gover,(0,0))
    pg.display.flip()
    sleep(3.5)

def change_vol(value):
    vol = value
    mixer.music.set_volume(vol)
    print("Changed game volume to", vol)
    
def pelin_aloitus():
    pg.display.flip()
    playerArea.left = 30
    playerArea.top = 723
    dispSurf.blit(level, (0,0))
    dispSurf.blit(player, playerArea)
    dispSurf.blit(ylakerta,(280,200))
    dispSurf.blit(alakerta,(280,725))
    pg.draw.rect(dispSurf, (255,255,255), border_top)
    pg.draw.rect(dispSurf, (255,255,255), border_btm)

    while True:
        # looppi joka tarkastaa jos pelaaja painaa esciä tai sulkee ikkunan
        for event in pg.event.get(): 
            if event.type == pg.QUIT: # jos pelaaja sulkee ikkunan((
                pg.quit()             # peli sulkeutuu
                sys.exit()    
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE: # jos pelaaja painaa esciä
                    menu()  # palaa takaisin päävalikkoon

            if event.type == KEYDOWN and event.key == K_DOWN:
                global press_down, press_up
                press_down = True
                press_up = False
            if event.type == KEYDOWN and event.key == K_UP:
                press_down = False
                press_up = True  
                    
        # Hahmon ohjaustoimintoja
        if press_down:
            playerArea.move_ip((0,2))
            dispSurf.blit(alanappi,(280,725))
            pg.display.flip()
        if press_up:
            playerArea.move_ip((0,-2))
            dispSurf.blit(ylanappi,(280,200))
            pg.display.flip()

        # Häviämistoiminnot
        if playerArea.y == border_top.y + border_top.height: #Jos pelaaja osuu ylärajaan, peli päättyy
            failup()
            game_over()
            break
            
        if playerArea.y == border_btm.y - playerArea.height: #Jos pelaaja osuu alarajaan, peli päättyy
            failbtm()
            game_over()
            break
        # renderöi kaikki objektit tarkoille paikoilleen
        dispSurf.blit(level, (0,0)) # jos tätä ei tehdä, kaikesta liikkuvasta jää niin sanottu jälki perään
        dispSurf.blit(player, playerArea)
        dispSurf.blit(ylakerta,(280,200))
        dispSurf.blit(alakerta,(280,725))
        pg.draw.rect(dispSurf, (255,255,255), border_top)
        pg.draw.rect(dispSurf, (255,255,255), border_btm)

        # tässä päivitetään esim. näppäimenpainallukset ruudulle aina loopin lopussa
        pg.display.flip()
        pass

def menu():
    menu = pygame_menu.Menu('Hissipeli', 1920, 1080, center_content=True, 
                            mouse_enabled=True, theme=pygame_menu.themes.THEME_DARK, menu_id="1",
                            )
    asetukset = pygame_menu.Menu('Asetukset', 1280, 720, center_content=True, 
                            mouse_enabled=True, theme=pygame_menu.themes.THEME_DARK, menu_id="2",)

    #Päävalikon määrittelyä
    menu.set_sound(sEngine, recursive=True)
    menu.add.button("Pelaa", pelin_aloitus)
    menu.add.button("Asetukset", asetukset,)
    menu.add.button("Lopeta", pygame_menu.events.EXIT)

    #Asetussivun määrittely
    asetukset.set_sound(sEngine, recursive=True)
    asetukset.add.range_slider('Äänenvoimakkuus', 0.5, (0.0,1), 0.1, 
                            value_format=lambda x: str((x)), onchange=change_vol) # äänenvoimakkuuden säätö, joka ottaa rangesliderin arvon, tallentaa sen muuttujaan value
                                                                                    # ja antaa sen funktiolle change_vol

    asetukset.add.button('Palaa päävalikkoon', pygame_menu.events.RESET)

    menu.mainloop(dispSurf)
menu()