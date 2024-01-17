import pygame as pg
import sqlite3

WIDTH1, HEIGHT1, FPS1 = (600,500,60)
#Define colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREY = (125,125,125)

pg.init()
pg.mixer.init()

#create the display
screen = pg.display.set_mode(( WIDTH1, HEIGHT1))
pg.display.set_caption('Sign in')
clock = pg.time.Clock()

#game loop
running = True
while running:
    clock.tick(FPS1)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    #Draw/render
    screen.fill(GREY)
    pg.display.flip()

pg.quit()