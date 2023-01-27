import pygame as pg
import pygame_menu
import sys
import ctypes
from pygame.locals import *
from pygame import mixer

pg.init()

#tekee näytön skaalauksesta mukautuvan jokaiselle resoluutiolle (alle full HD tuskin toimii kunnolla)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware(2)
width = 1920
lenght = 1080
dispSurf = pg.display.set_mode((width,lenght), vsync=1)
pg.display.set_caption("Hissipeli")


# kaikki renderöitävät objektit
level = pg.image.load("Hissipeli_ovet_kiinni.jpg").convert()
player = pg.image.load("laatikko.jpg").convert()
ylakerta = pg.image.load("ylakerta.png").convert()
ylanappi = pg.image.load("ylanappi.png")
alakerta = pg.image.load("alakerta.png").convert()
alanappi = pg.image.load("alanappi.jpg").convert()
fail1 = pg.image.load("Hissipeli_ylaovi_auki.jpg").convert
fail2 = pg.image.load("Hissipeli_alaovi_auki.jpg").convert

# pelaajan rajojen placeholderit
border_top = pg.Rect(30, 125, 325, 1)
border_btm = pg.Rect(30, 1015, 325, 1)

# otan hissien vieressä seisovien ukkelien kuvista taustat pois
ylakerta.set_colorkey((255, 255, 255))
ylanappi.set_colorkey((255,255,255))
alakerta.set_colorkey((255, 255, 255))
alanappi.set_colorkey((255, 255, 255))

dispSurf.blit(level, (0,0))
dispSurf.blit(player, (400,300))
dispSurf.blit(ylakerta,(200,300))
dispSurf.blit(ylanappi,(200, 300))
dispSurf.blit(alakerta,(500,600))
dispSurf.blit(alanappi,(500,600))

pg.display.flip()

playerArea = player.get_rect()

#pelaajan hahmon aloituspaikan liikuttaminen (pikseleissä)
playerArea.left = 100
playerArea.top = 800

""" mixer.init()
mixer.music.load('Doom.ogg')
mixer.music.play(-1)
 """
def pelin_aloitus():
    
    while True:
        # looppi joka tarkastaa jos pelaaja painaa esciä tai sulkee ikkunan
        for event in pg.event.get(): 
            if event.type == pg.QUIT: # jos pelaaja sulkee ikkunan
                pg.quit()             # peli sulkeutuu
                sys.exit()    
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE: # jos pelaaja painaa esciä
                    menu.mainloop(dispSurf)# palaa takaisin päävalikkoon
                    
        # Hahmon ohjaustoimintoja
        pressings = pg.key.get_pressed()
        if pressings[K_DOWN]:
            playerArea.move_ip((0,1))
            dispSurf.blit(alanappi,(280,725))
            pg.display.flip()
            
        if pressings[K_UP]:
            playerArea.move_ip((0,-1))
            dispSurf.blit(ylanappi,(280,200))
            pg.display.flip()
        
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

menu = pygame_menu.Menu('Hissipeli', 1920, 1080, center_content=True, 
                        mouse_enabled=True, theme=pygame_menu.themes.THEME_DARK, menu_id="1",
                        )
asetukset = pygame_menu.Menu('Asetukset', 1280, 720, center_content=True, 
                         mouse_enabled=True, theme=pygame_menu.themes.THEME_DARK, menu_id="2",)

#Päävalikon määrittelyä
menu.add.button("Pelaa", pelin_aloitus)
menu.add.button("Asetukset", asetukset,)
menu.add.button("Lopeta", pygame_menu.events.EXIT)

#Asetussivun määrittely
asetukset.add.range_slider('Äänenvoimakkuus', 50, (0,100), 1, 
                           value_format=lambda x: str(int(x))) #muokkaa sliderin näyttämään vain kokonaislukuja
asetukset.add.button('Palaa päävalikkoon', pygame_menu.events.RESET)

menu.mainloop(dispSurf)