import pygame as pg
import sqlite3 as sq

font_name = pg.font.match_font('arial')

def draw_text1(surf,text,size, x,y):
    #create a font oject
    font = pg.font.Font(font_name,size)
    #this will create text
    text_surface = font.render(text,True,RED)
    #true is for anti aliasing
    text_rect = text_surface.get_rect()
    #get rectagle for the text
    text_rect.midtop = (x,y)
    #put x,y at the midtop of the rectangle
    surf.blit(text_surface, text_rect)

def draw_text2(surf, text, size, x,y):
        #create a font oject
    font = pg.font.Font(font_name,size)
    #this will create text
    text_surface = font.render(text,True,RED)
    #true is for anti aliasing
    text_rect = text_surface.get_rect()
    #get rectagle for the text
    text_rect.midtop = (x,y)
    #put x,y at the midtop of the rectangle
    surf.blit(text_surface, text_rect)
