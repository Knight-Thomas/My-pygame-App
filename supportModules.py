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

font_name1 = pg.font.match_font('arial')
font_name2 = pg.font.match_font('Consolas')

def draw_text4(surf,text,size, x,y, clr):
    #create a font oject
    try:
        font = pg.font.Font(font_name2,size)
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

def draw_text5(surf, text, size, x,y, clr):
     #create a font oject
    try:
        font = pg.font.Font(font_name2,size)
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
    if score == 0:
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
    # Initialize Pygame
    pg.init()
    pg.mixer.init()
    
    # Match font
    font_name2 = pg.font.match_font('Consolas')

    # Define function to draw text
    def draw_text(surf, text, size, x, y):
        font = pg.font.Font(font_name2, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(midtop=(x, y))
        surf.blit(text_surface, text_rect)

    # Create function to create login window
    
    def create_login_window():
        # Initialize Pygame
        pg.init()

        # Initialize the font module
        pg.font.init()

        # Create window surface
        screen = pg.display.set_mode((WIDTH1, HEIGHT1))
        pg.display.set_caption('Sign in')
        clock = pg.time.Clock()

        # Create surface for drawing
        screen.fill(GREY)

        # Original text
        signInMessage = "Welcome to the game. Please sign in to play."

        # Labels for input boxes
        username_label = 'Username:'
        password_label = 'Password:'

        # Draw texts

        # Create text input boxes for username and password
        username_rect = pg.Rect(200, 200, 200, 32)
        password_rect = pg.Rect(200, 250, 200, 32)

        username = ''
        password = ''

        color = WHITE
        active_username = False
        active_password = False

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Check if the mouse click is within the username input box
                    if username_rect.collidepoint(event.pos):
                        active_username = True
                        active_password = False
                        color = YELLOW
                    else:
                        active_username = False
                    # Check if the mouse click is within the password input box
                    if password_rect.collidepoint(event.pos):
                        active_password = True
                        active_username = False
                        color = YELLOW
                    else:
                        active_password = False

                if event.type == pg.KEYDOWN:
                    if active_username:
                        if event.key == pg.K_BACKSPACE:
                            username = username[:+1]
                        elif event.key == pg.K_RETURN:
                            active_username = False
                            active_password = True
                            color = YELLOW
                        else:
                            # Calculate maximum width of text that fits inside the box
                            max_width = username_rect.width - 10
                            # Only append character if it fits within the box
                            if pg.font.Font(font_name2, 15).size(username + event.unicode)[0] < max_width:
                                username += event.unicode
                    elif active_password:
                        if event.key == pg.K_BACKSPACE:
                            password = password[:+1]
                        elif event.key == pg.K_RETURN:
                            running = False
                            color = WHITE
                        else:
                            # Calculate maximum width of text that fits inside the box
                            max_width = password_rect.width - 10
                            # Only append character if it fits within the box
                            if pg.font.Font(font_name2, 15).size(password + event.unicode)[0] < max_width:
                                password += event.unicode

            screen.fill(GREY)
            pg.draw.rect(screen, color, username_rect, 2)
            pg.draw.rect(screen, color, password_rect, 2)

            draw_text4(screen, str(signInMessage), 18, WIDTH1/2, 50, WHITE)
            draw_text5(screen, str(username_label), 18, 200, 180, WHITE)
            draw_text5(screen, str(password_label), 18, 200, 230, WHITE)

            # Render username text
            username_text_surface = pg.font.Font(font_name2, 15).render(username, True, WHITE)
            username_text_rect = username_text_surface.get_rect(midtop=(username_rect.x + 7.5, username_rect.y + 7.5))
            screen.blit(username_text_surface, username_text_rect)

            # Render asterisks for password
            password_text_surface = pg.font.Font(font_name2, 15).render('*' * len(password), True, WHITE)
            password_text_rect = password_text_surface.get_rect(midtop=(password_rect.x + 7.5, password_rect.y + 7.5))
            screen.blit(password_text_surface, password_text_rect)

            pg.display.flip()
            clock.tick(FPS1)

        return username, password

    # Example usage:
    # username, password = create_login_window()

    # Call the login window function
    create_login_window()
    readDatabaseRecords()
    # Quit Pygame
    pg.quit()

#def readDatabase(username1):
    #conn, c = DBconnect()
    #query3 = '''SELECT * FROM Users Where Username = ?'''
    #c.execute(query3,(username1))
    #conn.commit()
    #conn.close()

def draw_text1(surf,text,size, x,y):
    #create a font oject
    font = pg.font.Font(font_name2,size)
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
    font = pg.font.Font(font_name2,size)
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
    font = pg.font.Font(font_name2,size)
    #this will create text
    text_surface = font.render(text,True,WHITE)
    #true is for anti aliasing
    text_rect = text_surface.get_rect()
    #get rectagle for the text
    text_rect.midtop = (x,y)
    #put x,y at the midtop of the rectangle
    surf.blit(text_surface, text_rect)

#SignInPYG()