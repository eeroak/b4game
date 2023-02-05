import pygame as pg
import pygame_menu
import sys
import ctypes
from time import sleep
from pygame_menu import sound
from pygame.locals import *
from pygame import mixer

pg.init()

user32 = ctypes.windll.user32
user32.SetProcessDPIAware(2) #tekee näytön skaalauksesta mukautuvan jokaiselle resoluutiolle (alle full HD tuskin toimii kunnolla)
width = 1920
lenght = 1080
dispSurf = pg.display.set_mode((width,lenght), vsync=1)
pg.display.set_caption("Hissipeli")

# kaikki renderöitävät objektit
level = pg.image.load("Hissipeli_ovet_kiinni.jpg").convert()
player = pg.image.load("hissiukko ilo.png").convert()
ylakerta = pg.image.load("ylakerta.png").convert()
ylanappi = pg.image.load("ylanappi.png")
alakerta = pg.image.load("alakerta.png").convert()
alanappi = pg.image.load("alanappi.jpg").convert()
gover = pg.image.load("gameover.jpg").convert()
fail = pg.image.load("hissiukko_suru.png").convert()
hissi_auki_ala = pg.image.load("Hissipeli_alaovi_auki.jpg").convert()
hissi_auki_yla = pg.image.load("Hissipeli_ylaovi_auki.jpg").convert()

# pelin rajat
border_top = pg.Rect(30, 220, 325, 1)
border_btm = pg.Rect(30, 1015, 325, 1)

# otan hissien vieressä seisovien ukkelien kuvista taustat pois
ylakerta.set_colorkey((255,255,255))
ylanappi.set_colorkey((255,255,255))
alakerta.set_colorkey((255,255,255))
alanappi.set_colorkey((255,255,255))
player.set_colorkey((255,255,255))
fail.set_colorkey((255,255,255))

#pelaajan hahmon aloituspaikan liikuttaminen (pikseleissä)
playerArea = player.get_rect()
playerArea.left = 30
playerArea.top = 723

# pelin taustaäänet/valikkoäänet
mixer.init() 
mixer.music.load('Doom.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.1) # oletusäänenvoimakkuus
sEngine = sound.Sound()
sEngine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION,('menuselect.ogg'))
sEngine.set_sound(sound.SOUND_TYPE_CLOSE_MENU,('menuselect.ogg'))

press_down = False
press_up = False

def failup():
    global fail, press_up
    fail.set_colorkey((255,255,255))
    dispSurf.blit(hissi_auki_yla,(0,0))
    dispSurf.blit(ylakerta,(280,200))
    dispSurf.blit(alakerta,(280,725))
    dispSurf.blit(fail,(playerArea))
    pg.display.flip()
    press_up=False
    pg.time.wait(2500)

def failbtm():
    global press_down, fail
    player.set_colorkey((255,255,255))
    dispSurf.blit(hissi_auki_ala,(0,0))
    dispSurf.blit(ylakerta,(280,200))
    dispSurf.blit(alakerta,(280,725))
    dispSurf.blit(fail, (playerArea))
    pg.display.flip()
    press_down = False
    pg.time.wait(2500)

def game_over():
    print("game over")
    dispSurf.blit(gover,(0,0))
    pg.display.flip()
    sleep(3.5)

def change_vol(value):
    vol = value
    mixer.music.set_volume(vol)
    
def pelin_aloitus():
    player = pg.image.load("hissiukko ilo.png").convert()
    player.set_colorkey((255,255,255))
    playerArea.left = 30
    playerArea.top = 723
    dispSurf.blit(level, (0,0))
    dispSurf.blit(player, (playerArea))
    dispSurf.blit(ylakerta,(280,200))
    dispSurf.blit(alakerta,(280,725))
    pg.draw.rect(dispSurf, (255,255,255), border_top)
    pg.draw.rect(dispSurf, (255,255,255), border_btm)

    while True:

        # looppi joka tarkastaa näppäimien painalluksia
        for event in pg.event.get(): 
            if event.type == pg.QUIT: # jos pelaaja sulkee ikkunan
                pg.quit()             # peli sulkeutuu ))
                sys.exit()    
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE: # jos pelaaja painaa esciä
                    menu()                # peli palaa takaisin päävalikkoon
                    
            if event.type == KEYDOWN and event.key == K_DOWN:
                global press_down, press_up
                press_down = True
                press_up = False
            if event.type == KEYDOWN and event.key == K_UP:
                press_down = False
                press_up = True

        # Hahmon ohjaustoimintoja
        if press_down:
            playerArea.move_ip((0,1))
            dispSurf.blit(alanappi,(280,725))
            pg.display.flip()
        if press_up:
            playerArea.move_ip((0,-1))
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
    mytheme = pygame_menu.themes.THEME_DARK.copy()
    myimage = pygame_menu.baseimage.BaseImage(("Hissipeli.jpg"),
        drawing_mode = pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage
    menu = pygame_menu.Menu("",1920, 1080, center_content=True, 
                            mouse_enabled=True, theme=mytheme, menu_id="1",
                            )
    asetukset = pygame_menu.Menu('Asetukset', 1280, 720, center_content=True, 
                            mouse_enabled=True, theme=pygame_menu.themes.THEME_DARK, menu_id="2",)
    ohjeet = pygame_menu.Menu ('Peliohjeet', 1280, 720, center_content=True,
                           mouse_enabled=True, theme=pygame_menu.themes.THEME_DARK, menu_id="3",)                        

    #Päävalikon määrittelyä
    menu.set_sound(sEngine, recursive=True)
    menu.add.button("Pelaa", pelin_aloitus,background_color=(157,11,14),border_color = (0,0,0),border_width=(5),font_color =(0,0,0))
    menu.add.label("")
    menu.add.button("Asetukset", asetukset,background_color=(157,11,14),border_color=(0,0,0),border_width=(5),font_color=(0,0,0))
    menu.add.label("")
    menu.add.button("Peliohjeet", ohjeet,background_color=(157,11,14),border_color=(0,0,0),border_width=(5),font_color=(0,0,0))
    menu.add.label("")
    menu.add.button("Lopeta", pygame_menu.events.EXIT,background_color=(157,11,14),border_color=(0,0,0),border_width=(5),font_color=(0,0,0))
    
    #Asetussivun määrittely
    asetukset.set_sound(sEngine, recursive=True)
    asetukset.add.range_slider('Äänenvoimakkuus', 0.5, (0.0,1), 0.1, 
                            value_format=lambda x: str((x)), onchange=change_vol) # äänenvoimakkuuden säätö, joka ottaa rangesliderin arvon, tallentaa sen muuttujaan value ja antaa sen funktiolle change_vol
    asetukset.add.button('Palaa päävalikkoon', pygame_menu.events.RESET)
    
    # Peliohjeet
    ohjeet.set_sound(sEngine, recursive=True)
    ohjeet.add.label("Paina NUOLIALAS näppäintä ennen kuin hissi saavuttaa ylärajan",font_size=(35))
    ohjeet.add.label("Paina NUOLIYLÖS näppäintä ennen kuin hissi saavuttaa alarajan",font_size=(35),padding=(25,100,200,100)) #top, right, bottom, left
    ohjeet.add.button('Palaa päävalikkoon',pygame_menu.events.RESET)

    menu.mainloop(dispSurf)
menu()