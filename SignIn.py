import pygame as pg
import sqlite3
import sys

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

font_name = pg.font.match_font('Consolas')

new_db = sqlite3.connect("Ian-Hawke-Game.db")
c = new_db.cursor()

def draw_text1(surf,text,size, x,y):
    #create a font oject
    font = pg.font.Font(font_name,size)
    #this will create text
    text_surface = font.render(text,True,WHITE)
    #true is for anti aliasing
    text_rect = text_surface.get_rect()
    #get rectagle for the text
    text_rect.midtop = (x,y)
    #put x,y at the midtop of the rectangle
    surf.blit(text_surface, text_rect)

def draw_text2(surf,text,size, x,y):
    #create a font oject
    font = pg.font.Font(font_name,size)
    #this will create text
    text_surface = font.render(text,True,WHITE)
    #true is for anti aliasing
    text_rect = text_surface.get_rect()
    #get rectagle for the text
    text_rect.midtop = (x,y)
    #put x,y at the midtop of the rectangle
    surf.blit(text_surface, text_rect)

def draw_text3(surf,text,size, x,y):
    #create a font oject
    font = pg.font.Font(font_name,size)
    #this will create text
    text_surface = font.render(text,True,WHITE)
    #true is for anti aliasing
    text_rect = text_surface.get_rect()
    #get rectagle for the text
    text_rect.midtop = (x,y)
    #put x,y at the midtop of the rectangle
    surf.blit(text_surface, text_rect)


#create a sprite group
all_sprites = pg.sprite.Group()

text1 = '''Please sign in to play'''
text2 = '''If you do not have an account you can make one'''
text3 = '''Just sign in like normal and an account will be made for you'''

#game loop
running = True
while running:
    clock.tick(FPS1)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    #update
    all_sprites.update()

    #Draw/render
    screen.fill(GREY)
    all_sprites.draw(screen)
    draw_text1(screen,str(text1),15,WIDTH1/2,10)
    draw_text2(screen,str(text2),15,WIDTH1/2,30)
    draw_text3(screen,str(text3),15,WIDTH1/2,50)
    pg.display.flip()

Username = input('Enter Username: ')
Password = input('Enter Password: ')


c.execute('''INSERT INTO Users
          VALUES (?,?,0)''', (Username, Password))


if Username and Password != '':
    pg.QUIT
else:
    print('Invalid')

new_db.commit()
new_db.close()