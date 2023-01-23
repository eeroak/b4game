import pygame
import sys     # sys-module will be needed to exit the game
from pygame.locals import * # imports the constants of pygame
pygame.init()  # initializes pygame

# the display surface
width = 960
height = 600
dispSurf = pygame.display.set_mode((width,height))
pygame.display.set_caption("My game")

# the Surface objects
level = pygame.image.load("level.jpg").convert()
mario = pygame.image.load("mario.png").convert()
fireball = pygame.image.load("fireball.png").convert()
# pygame.image.load(file) function loads a picture "file" into a given variable
# convert() method converts the picture into the right pixel-format
# picture files needs to be in the same folder as this python file
# the folder path can be relative or absolute:
# relative path: mario = pygame.image.load("folder\\mario.png").convert()
# absolute path: fireball = pygame.image.load("C:\\folder\\fireball.png").convert()

# empty black Surface(width, height)
rectangle = pygame.Surface((300,50))

# RGB-colors are tuples (r,g,b), where 0<r,g,b<255
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pink = (255,0,130)

# Surface objects can be filled with a color using fill() method
rectangle.fill(pink)

# Surface objects can be added to the display surface with blit() method
# blit(Surface,(x,y)) adds "Surface" into coordinates (x,y)=(left, top)
dispSurf.blit(level, (0,0))
dispSurf.blit(fireball, (0,0))
dispSurf.blit(mario, (400,500))
dispSurf.blit(rectangle, (0,200))

# the display surface needs to be updated for the blitted Surfaces to become visible
# pygame.display.update() would do the same
pygame.display.flip()

# Surface.get_rect() method returns the Rect object of "Surface"
# Rect objects are needed to move Surfaces and for collision detection
# Rect(left, top, width, height) contains left/top-coordinates and width/height
fireballArea = fireball.get_rect()
marioArea = mario.get_rect()
rectangleArea = rectangle.get_rect()

# get_rect() method by default sets the left-top corner to (0,0)
# mario and rectangle were not blitted into (0,0)
# the left and top coordinates have to be changed with dot notation
marioArea.left = 400
marioArea.top = 500
rectangleArea.left = 0
rectangleArea.top = 200

# speed contains the [x,y]-speed of the fireball in pixels
speed = [1,1]





# the game loop which runs until sys.exit()
while True:


    # loop to check if the user has closed the display window or pressed esc
    for event in pygame.event.get():  # list of all the events in the event queue
        if event.type == pygame.QUIT: # if the player closed the window
            pygame.quit() # the display window closes
            sys.exit()    # the python program exits
        if event.type == KEYDOWN:     # if the player pressed down any key
            if event.key == K_ESCAPE: # if the key was esc
                pygame.quit() # the display window closes
                sys.exit()    # the python program exits


    # fireball will be moved by speed=[1,1] in every iteration
    # move_ip([x,y]) changes the Rect-objects left-top coordinates by x and y
    fireballArea.move_ip(speed)


    # fireball bounces from the edges of the display surface
    if fireballArea.left < 0 or fireballArea.right > width: # fireball is vertically outside the game
        speed[0] = -speed[0] # the x-direction of the speed will be converted
    if fireballArea.top < 0 or fireballArea.bottom > height: # fireball is horizontally outside the game
        speed[1] = -speed[1] # the y-direction of the speed will be converted


    # fireball bounces from the rectangle
    if rectangleArea.colliderect(fireballArea):
    # a.colliderect(b) returns True if Rect-objects a and b overlap
        if rectangleArea.colliderect(fireballArea.move(-speed[0],0)):
        # if the fireball came from vertical direction
            speed[1] = -speed[1] # the y-direction of the speed will be converted
        else:
        # otherwise the fireball came from horizontal direction
            speed[0] = -speed[0] # the x-direction of the speed will be converted


    # mario can be moved with left/right/up/down-keys
    # get.pressed() function gives a boolean list of all the keys if they are being pressed
    pressings = pygame.key.get_pressed()
    if pressings[K_LEFT]:          # if left-key is true in the list
        marioArea.move_ip((-1,0))  # mario will be moved one pixel left
    if pressings[K_RIGHT]:
        marioArea.move_ip((1,0))
    if pressings[K_DOWN]:
        marioArea.move_ip((0,1))
    if pressings[K_UP]:
        marioArea.move_ip((0,-1))


    # blit all the Surfaces in their new places
    dispSurf.blit(level, (0,0)) # without this, moving characters would have a "trace"
    dispSurf.blit(fireball, fireballArea)
    dispSurf.blit(mario, marioArea)
    dispSurf.blit(rectangle, rectangleArea)


    # updating the display surface is always needed at the end of each iteration of game loop
    pygame.display.flip()

