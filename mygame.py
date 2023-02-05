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
voitto = pg.image.load("voitto.jpg").convert()
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
sEngine = sound.Sound()
sEngine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION,('menuselect.ogg'))
sEngine.set_sound(sound.SOUND_TYPE_CLOSE_MENU,('menuselect.ogg'))

press_down = False
press_up = False

#pistelaskurin graafinen esitysmäärittely
black = (0,0,0)
scorefont = pg.font.SysFont("comicsansmms", size=40)
points = 0

# pistelaskuri
def score():
    global points
    text = scorefont.render("SCORE: "+ str(points), True, black)
    dispSurf.blit(text, (125,20))
    pg.display.flip()
    
# funktio pelin resetoimiselle jos pelaaja osuu ylärajaan
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
    
# funktio pelin resetoimiselle jos pelaaja osuu alarajaan
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
    
# game-over ruudun rendröintifunktio, mikäli pelaaja osuu rajoihin
def game_over():
    dispSurf.blit(gover,(0,0))
    pg.display.flip()
    sleep(3.5)
    
# pelin voittoruudun renderöintifunktio, mikäli pelaaja voittaa pelin
def game_win():
    global press_down, press_up
    dispSurf.blit(voitto,(0,0))
    pg.display.flip()
    press_down = False
    press_up=False
    sleep(3.5)

def change_vol(value):
    vol = value
    mixer.music.set_volume(vol)
    
def pelin_aloitus():
    #resetoi aina pelin alussa kaikki oleelliset asiat
    pg.init()
    global points
    pg.display.flip()
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
    vel = 1.0
    points = 0
    
    # varsinainen pelin "aloitus"
    while True:
        # looppi joka tarkastaa näppäimien painalluksia
        for event in pg.event.get(): 
            if event.type == pg.QUIT: # jos pelaaja sulkee ikkunan
                pg.quit()             # peli sulkeutuu ))
                sys.exit()    
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE: # jos pelaaja painaa esciä
                    menu()                # peli palaa takaisin päävalikkoon
                    
            # liikkumissysteemi ja pistelaskuri nappien painalluksilla        
            if event.type == KEYDOWN and event.key == K_DOWN:
                global press_down, press_up
                points+=1
                press_down = True
                press_up = False
            if event.type == KEYDOWN and event.key == K_UP:
                points+=1
                press_down = False
                press_up = True
    
        # pelin voittomääritykset, jos pelaaja saa 100 pistettä, peli loppuu           
        if points > 10:
            vel = 2
        if points > 20:
            vel = 3
        if points > 40:
            vel = 4
        if points > 50:
            vel = 5
        if points > 100:
            game_win()
            break
        
        # pelihahmon liikuttamisen nopeudet
        if press_down:
            playerArea.move_ip((0,vel))
            dispSurf.blit(alanappi,(280,725))
            pg.display.flip()
        if press_up:
            playerArea.move_ip((0,-vel))
            dispSurf.blit(ylanappi,(280,200))
            pg.display.flip()

        # Häviämistoiminnot
        if playerArea.y <= border_top.y + border_top.height - vel: #Jos pelaaja osuu ylärajaan, peli päättyy
            failup()
            game_over()
            break
        if playerArea.y >= border_btm.y - playerArea.height: #Jos pelaaja osuu alarajaan, peli päättyy
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
        
        score()
        pg.display.flip()
        pass

def menu():
    # pelin musiikki
    mixer.init() 
    mixer.music.load('Doom.ogg')
    mixer.music.play(-1)
    mixer.music.set_volume(0.1)
    
    #kustomoitu teema peliin
    mytheme = pygame_menu.themes.THEME_DARK.copy()
    myimage = pygame_menu.baseimage.BaseImage(("Hissipeli.jpg"),
        drawing_mode = pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage
    
    # tässä luodaan 3 eri valikkoa 
    menu = pygame_menu.Menu("",1920, 1080, center_content=True, 
                            mouse_enabled=True, theme=mytheme, menu_id="1",
                            )
    asetukset = pygame_menu.Menu('Asetukset', 1920, 1080, center_content=True, 
                            mouse_enabled=True, theme=mytheme, menu_id="2",)
    ohjeet = pygame_menu.Menu ('Peliohjeet', 1920, 1080, center_content=True,
                           mouse_enabled=True, theme=mytheme, menu_id="3",)                        

    #Päävalikon määrittelyä
    menu.set_sound(sEngine, recursive=True)
    menu.add.button("Pelaa",pelin_aloitus,background_color=(157,11,14),border_color = (0,0,0),border_width=(5),font_color =(0,0,0))
    menu.add.label("")
    menu.add.button("Asetukset",asetukset,background_color=(157,11,14),border_color=(0,0,0),border_width=(5),font_color=(0,0,0))
    menu.add.label("")
    menu.add.button("Peliohjeet",ohjeet,background_color=(157,11,14),border_color=(0,0,0),border_width=(5),font_color=(0,0,0))
    menu.add.label("")
    menu.add.button("Lopeta",pygame_menu.events.EXIT,background_color=(157,11,14),border_color=(0,0,0),border_width=(5),font_color=(0,0,0))
    
    #Asetussivun määrittely
    asetukset.set_sound(sEngine, recursive=True)
    asetukset.add.range_slider('Äänenvoimakkuus', 0.1, (0.0,1), 0.1, 
                            value_format=lambda x: str((x)), onchange=change_vol, background_color=(157,11,14),border_width=(5),font_color=(0,0,0)) # äänenvoimakkuuden säätö, joka ottaa rangesliderin arvon, tallentaa sen muuttujaan value ja antaa sen funktiolle change_vol
    asetukset.add.label("")
    asetukset.add.button('Palaa päävalikkoon', pygame_menu.events.RESET, background_color=(157,11,14),border_color=(0,0,0),border_width=(5),font_color=(0,0,0))
    
    # Peliohjeet- sivun määrittely
    ohjeet.set_sound(sEngine, recursive=True)
    ohjeet.add.label("Pelin voittaa kun saavuttaa 100 pistettä",font_size=(35),font_color=(0,0,0),background_color=(157,11,14),padding=(0,280,0,300))
    ohjeet.add.label("Jokaisesta painalluksesta saa yhden pisteen",font_size=(35),font_color=(0,0,0),background_color=(157,11,14),padding=(0,306,0,200))
    ohjeet.add.label("Paina NUOLIALAS näppäintä ennen kuin hissi saavuttaa ylärajan",font_size=(35),font_color=(0,0,0),background_color=(157,11,14),padding=(0,83,0,100))
    ohjeet.add.label("Paina NUOLIYLÖS näppäintä ennen kuin hissi saavuttaa alarajan",font_size=(35),font_color=(0,0,0),background_color=(157,11,14),padding=(0,80,0,100))
    ohjeet.add.label("")
    ohjeet.add.button('Palaa päävalikkoon',pygame_menu.events.RESET,background_color=(157,11,14),border_color=(0,0,0),border_width=(5),font_color=(0,0,0))

    menu.mainloop(dispSurf)
menu()
