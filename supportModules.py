import pygame as pg
import sqlite3 as sq
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

font_name = pg.font.match_font('arial')

def draw_text1(surf,text,size, x,y, clr):
    #create a font oject
    try:
        font = pg.font.Font(font_name,size)
        #this will create text
        text_surface = font.render(text,True,clr)
        #true is for anti aliasing
        text_rect = text_surface.get_rect()
        #get rectagle for the text
        text_rect.midtop = (x,y)
        #put x,y at the midtop of the rectangle
        surf.blit(text_surface, text_rect)
    except pg.error as e:
        print(f'Pygame Error: {e}')

def draw_text2(surf, text, size, x,y, clr):
     #create a font oject
    try:
        font = pg.font.Font(font_name,size)
        #this will create text
        text_surface = font.render(text,True,clr)
        #true is for anti aliasing
        text_rect = text_surface.get_rect()
        #get rectagle for the text
        text_rect.midtop = (x,y)
        #put x,y at the midtop of the rectangle
        surf.blit(text_surface, text_rect)
    except pg.error as e:
        print(f'Pygame Error: {e}')

def DBconnect():
    try:
        conn = sq.connect("Ian-Hawke-Game.db")
        c = conn.cursor()
        return conn, c
    except sq.Error as e:
        print(f'Database conection error: {e}')
    
def writeNewToDatabase(Username, Password, score):
    '''writes to the database'''
    if score == '':
        score = 0
    else:
        score = score
    conn, c = DBconnect()
    c.execute('''INSERT INTO Users
          VALUES (?,?,0)''', (Username, Password, score))
    conn.commit()
    conn.close()
    print('success')

def readDatabaseRecords():
    '''Reads records from a database'''
    conn, c = DBconnect()
    query = """SELECT * FROM Users"""
    c.execute(query)
    results = c.fetchall()
    print(results)
    conn.close()

def writesToSpecific(Username, Password):
    '''writes a value to a specific record'''
    #query option to be written too
    query ="""SELECT COUNT(*)
            FROM Users
            WHERE Username =? """
    #prepare data to be written
    #open connection, write data, close connection
    conn, c = DBconnect()
    c.execute(query,(Username))
    results = c.fetchall()
    if results[0][0] ==1:
        print('call append method')
    else:
        writeNewToDatabase(Username, Password)
    conn.commit()
    conn.close()


def SignInPYG():
    pg.init()
    pg.mixer.init()

    #create the display
    screen = pg.display.set_mode(( WIDTH1, HEIGHT1))
    pg.display.set_caption('Sign in')
    clock = pg.time.Clock()

    font_name = pg.font.match_font('Consolas')

    conn = sq.connect("Ian-Hawke-Game.db")
    c = conn.cursor()

    #create a sprite group
    all_sprites = pg.sprite.Group()

    text1 = '''Please sign in to play'''
    text2 = '''If you do not have an account you can make one'''
    text3 = '''Just sign in like normal and an account will be made for you'''

    base_font = pg.font.Font(None, 32) 
    user_text = '' 

    input_rect = pg.Rect(200, 200, 140, 32)

    color_active = pg.Color(WHITE) 

    color_passive = pg.Color(WHITE) 
    color = color_passive

    active = False

    #game loop
    running = True
    while running:
        clock.tick(FPS1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit() 
                sys.exit() 
            # if user types QUIT then the screen will close 
  
            if event.type == pg.MOUSEBUTTONDOWN: 
                if input_rect.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False
  
        if event.type == pg.KEYDOWN: 
  
                # Check for backspace 
            if event.key == pg.K_BACKSPACE: 
  
                # get text input from 0 to -1 i.e. end. 
                user_text = user_text[:-1] 
  
            # Unicode standard is used for string 
            # formation 
            else: 
                user_text += event.unicode

    if active: 
        color = color_active 
    else: 
        color = color_passive

    #update
    all_sprites.update()

    #Draw/render
    pg.draw.rect(screen, color, input_rect)
    screen.fill(GREY)
    all_sprites.draw(screen)
    text_surface = base_font.render(user_text, True, (BLACK)) 
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    input_rect.w = max(100, text_surface.get_width()+10) 
    draw_text1(screen,str(text1),15,WIDTH1/2,10)
    draw_text2(screen,str(text2),15,WIDTH1/2,30)
    draw_text3(screen,str(text3),15,WIDTH1/2,50)
    pg.display.flip()

    Username = input('Enter Username: ')
    Password = input('Enter Password: ')

    query1 = '''SELECT Highscore FROM USERS
              WHERE Username = ?'''

    c.execute(query1,(Username))


    if Username and Password != '':
        pg.QUIT
    else:
        print('Invalid')

    conn.commit()
    conn.close()

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

SignInPYG()