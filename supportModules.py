import pygame as pg
import sqlite3 as sq


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
    conn, c = DBconnect()
    c.execute('''INSERT INTO Users
          VALUES (?,?,0)''', (Username, Password))
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

def writesToSpecific():
    '''writes a value to a specific record'''
    #query option to be written too
    query ="""SELECT COUNT(*)
            FROM Users
            WHERE Username ='Thomasknight1234' """
    #prepare data to be written
    #open connection, write data, close connection
    conn, c = DBconnect()
    c.execute(query)
    results = c.fetchall()
    if results[0][0] ==1:
        print('call append method')
    else:
        print('write new record')
    conn.commit()
    conn.close()