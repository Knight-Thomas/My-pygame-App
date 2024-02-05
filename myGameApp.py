#imports
import pygame as pg
import random
import sqlite3

from os import path
from supportModules import *
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__),'snd')

 
'''idea: chamge the dave sevill photo so its lookoing what way its going'''
'''create  database where a username and password is required to login and theyre high score will be stored in this database and will be updated if they beat it'''


#parameters
WIDTH, HEIGHT, FPS = (800,600,60)
WIDTH1, HEIGHT1, FPS1 = (600,500,60)
#define colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#Initialise common pygame objects
pg.init()  
pg.mixer.init()
background_sound1 = pg.mixer.Sound(path.join(snd_dir,'Alvin-Funkytown.mp3'))
background_sound1.play(60)     
#create the display
screen = pg.display.set_mode(( WIDTH, HEIGHT))
pg.display.set_caption('My Game')
clock = pg.time.Clock()
background = pg.image.load(path.join(img_dir,"UncleIan.jpeg")).convert()
background_rect = background.get_rect()
#load other images
player_img = pg.image.load(path.join(img_dir, "Dave-Seville.jpeg")).convert()
bullet_img = pg.image.load(path.join(img_dir, 'Alvin-Seville.TIFF')).convert()
mob_img = pg.image.load(path.join(img_dir, 'James-Suggs.TIFF')).convert() 
bullet_imgT = pg.image.load(path.join(img_dir, 'Theodore-Seville.TIFF')).convert()
bullet_imgS = pg.image.load(path.join(img_dir, 'Simon-Seville.TIFF'))


#a sprite will be an object which inherits from the built in sprite class
class Player(pg.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        #constructor
        pg.sprite.Sprite.__init__(self) #inheritance
        #self.image = pg.Surface((50,40))
        #self.image.fill(GREEN)
        self.image = pg.transform.scale(player_img,(50,38))
        #useful for moving, size, position and collision
        self.rect = self.image.get_rect()  #looks at the image and gets its rect
        self.rect.centerx = WIDTH/2 #places image in the centre
        self.rect.bottom = HEIGHT-10 #puts it in 10px from bottom of screen
        #it needs to move side to side so we need speed
        self.speedx = 0

    def update(self):
        #we will keep the default speed of object to zero and only alter it with a key press
        #this way we avoid coding for what happens when the key is released
        self.speedx = 0
        keystate = pg.key.get_pressed() #returned a list of keys that are down
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5   
        self.rect.x += self.speedx #move at speed to be set by controls
        #to ensure it does not run off the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        #spawns new bullet at centerx of player
        #y will spawn at the top - i.e. bottom of the bullet at the top of the player
        bullet = Bullet(self.rect.centerx,self.rect.top)
        #add bullet to all sprites grouo so that its updated
        all_sprites.add(bullet)
        #add bullet to the bullets sprite group
        bullets.add(bullet)

class Mob(pg.sprite.Sprite):
    #enemy mobile object which inherits from the sprite
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.Surface((30,40))
        #self.image.fill(RED)
        self.image = pg.transform.scale(mob_img,(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
       
        #make the enemy spawn off top of screen to appear off thescreen and then start dropping down
        self.rect.x = random.randrange(0,WIDTH - self.rect.width) #appears within the limits of the screen
        self.rect.y = random.randrange(-100,-40) #this is off the screen
        self.speedy = random.randrange(1,8)
    def update(self):
        #move downwards
        self.rect.y += self.speedy
        #deal with enemy when they get to bottom of the screen
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
            self.rect.y = random.randrange(-100,-40) #this is off the screen
            self.speedy = random.randrange(1,8)

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        #x and y and respawn positions based on the player's position
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.Surface((10,20))
        #self.image.fill(YELLOW)
        self.image = pg.transform.scale(bullet_img,(20,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #set respawn position to right in front of the player
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        #rect moves upwards at the speed
        self.rect.y += self.speedy
        #kill it if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

#create a sprite group
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()  #creating another group would aid during collision detection
bullets = pg.sprite.Group()  
#instatiate the player object and add it to the sprite group
player = Player()
#Spawn some mobs
for i in range(8):  
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)

all_sprites.add(player)
score = 0
text2 = ''
#game loop
running = True
while running:
    #keep the game running at the right speed
    clock.tick(FPS)
    #process input (events)
    for event in pg.event.get():
        #check event for closing the window
        if event.type == pg.QUIT:
            running = False
        #check event for keydown to shoot
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
   
    #load all game graphics
    #convert() methods will draw the image in memory before it is displayed which is
    #much fast than drawing it in real time .e. pixel by pixel
    #update
    all_sprites.update()
    #Check if a bullet hits a mob
    hits = pg.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score +=1 
        #1 point for every hit you make
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    if score == 0:
        text2 = 'LEVEL 1'
        draw_text2(screen,str(text2),18,WIDTH/2,30, RED)
    
    elif score == 100:
        class Bullet(pg.sprite.Sprite):
            def __init__(self,x,y):
                #x and y and respawn positions based on the player's position
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((10,20))
                #self.image.fill(YELLOW)
                self.image = pg.transform.scale(bullet_imgS,(20,50))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                #set respawn position to right in front of the player
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -15
            def update(self):
                #rect moves upwards at the speed
                self.rect.y += self.speedy
                #kill it if it moves off the top of the screen
                if self.rect.bottom < 0:
                    self.kill()
        class Mob(pg.sprite.Sprite):
            #enemy mobile object which inherits from the sprite
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((30,40))
                #self.image.fill(RED)
                self.image = pg.transform.scale(mob_img,(50,50))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
       
                #make the enemy spawn off top of screen to appear off thescreen and then start dropping down
                self.rect.x = random.randrange(0,WIDTH - self.rect.width) #appears within the limits of the screen
                self.rect.y = random.randrange(-100,-40) #this is off the screen
                self.speedy = random.randrange(1,15)
            def update(self):
                #move downwards
                self.rect.y += self.speedy
                #deal with enemy when they get to bottom of the screen
                if self.rect.top > HEIGHT + 10:
                    self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
                    self.rect.y = random.randrange(-100,-40) #this is off the screen
                    self.speedy = random.randrange(1,15)
        text2 = 'LEVEL 2'
        draw_text2(screen,str(text2),18,WIDTH/2,30, RED)
        
    elif score == 300:
        class Bullet(pg.sprite.Sprite):
            def __init__(self,x,y):
                #x and y and respawn positions based on the player's position
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((10,20))
                #self.image.fill(YELLOW)
                self.image = pg.transform.scale(bullet_img,(20,40))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                #set respawn position to right in front of the player
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -10
            def update(self):
                #rect moves upwards at the speed
                self.rect.y += self.speedy
                #kill it if it moves off the top of the screen
                if self.rect.bottom < 0:
                    self.kill()
        class Mob(pg.sprite.Sprite):
            #enemy mobile object which inherits from the sprite
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((30,40))
                #self.image.fill(RED)
                self.image = pg.transform.scale(mob_img,(50,50))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
       
                #make the enemy spawn off top of screen to appear off thescreen and then start dropping down
                self.rect.x = random.randrange(0,WIDTH - self.rect.width) #appears within the limits of the screen
                self.rect.y = random.randrange(-100,-40) #this is off the screen
                self.speedy = random.randrange(1,15)
            def update(self):
                #move downwards
                self.rect.y += self.speedy
                #deal with enemy when they get to bottom of the screen
                if self.rect.top > HEIGHT + 10:
                    self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
                    self.rect.y = random.randrange(-100,-40) #this is off the screen
                    self.speedy = random.randrange(1,15)
        text2 = 'LEVEL 4'
        draw_text2(screen,str(text2),18,WIDTH/2,30,RED)
            
    elif score == 200:
        class Bullet(pg.sprite.Sprite):
            def __init__(self,x,y):
                #x and y and respawn positions based on the player's position
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((10,20))
                #self.image.fill(YELLOW)
                self.image = pg.transform.scale(bullet_imgT,(70,80))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                #set respawn position to right in front of the player
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -5
            def update(self):
                #rect moves upwards at the speed
                self.rect.y += self.speedy
                #kill it if it moves off the top of the screen
                if self.rect.bottom < 0:
                    self.kill()
        class Mob(pg.sprite.Sprite):
            #enemy mobile object which inherits from the sprite
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((30,40))
                #self.image.fill(RED)
                self.image = pg.transform.scale(mob_img,(50,50))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
       
                #make the enemy spawn off top of screen to appear off thescreen and then start dropping down
                self.rect.x = random.randrange(0,WIDTH - self.rect.width) #appears within the limits of the screen
                self.rect.y = random.randrange(-100,-40) #this is off the screen
                self.speedy = random.randrange(1,20)
            def update(self):
                #move downwards
                self.rect.y += self.speedy
                #deal with enemy when they get to bottom of the screen
                if self.rect.top > HEIGHT + 10:
                    self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
                    self.rect.y = random.randrange(-100,-40) #this is off the screen
                    self.speedy = random.randrange(1,20)
        text2 = 'LEVEL 3'
        draw_text2(screen,str(text2),18,WIDTH/2,30, RED)   

    elif score == 600:
        class Bullet(pg.sprite.Sprite):
            def __init__(self,x,y):
                #x and y and respawn positions based on the player's position
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((10,20))
                #self.image.fill(YELLOW)
                self.image = pg.transform.scale(bullet_img,(20,40))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                #set respawn position to right in front of the player
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -10
            def update(self):
                #rect moves upwards at the speed
                self.rect.y += self.speedy
                #kill it if it moves off the top of the screen
                if self.rect.bottom < 0:
                    self.kill()
        class Mob(pg.sprite.Sprite):
            #enemy mobile object which inherits from the sprite
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((30,40))
                #self.image.fill(RED)
                self.image = pg.transform.scale(mob_img,(50,50))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
       
                #make the enemy spawn off top of screen to appear off thescreen and then start dropping down
                self.rect.x = random.randrange(0,WIDTH - self.rect.width) #appears within the limits of the screen
                self.rect.y = random.randrange(-100,-40) #this is off the screen
                self.speedy = random.randrange(1,30)
            def update(self):
                #move downwards
                self.rect.y += self.speedy
                #deal with enemy when they get to bottom of the screen
                if self.rect.top > HEIGHT + 10:
                    self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
                    self.rect.y = random.randrange(-100,-40) #this is off the screen
                    self.speedy = random.randrange(1,30)
        text2 = 'LEVEL 7'
        draw_text2(screen,str(text2),18,WIDTH/2,30, RED)

    elif score == 400:
        class Bullet(pg.sprite.Sprite):
            def __init__(self,x,y):
                #x and y and respawn positions based on the player's position
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((10,20))
                #self.image.fill(YELLOW)
                self.image = pg.transform.scale(bullet_imgS,(20,50))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                #set respawn position to right in front of the player
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -15
            def update(self):
                #rect moves upwards at the speed
                self.rect.y += self.speedy
                #kill it if it moves off the top of the screen
                if self.rect.bottom < 0:
                    self.kill()
        class Mob(pg.sprite.Sprite):
            #enemy mobile object which inherits from the sprite
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((30,40))
                #self.image.fill(RED)
                self.image = pg.transform.scale(mob_img,(50,50))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
       
                #make the enemy spawn off top of screen to appear off thescreen and then start dropping down
                self.rect.x = random.randrange(0,WIDTH - self.rect.width) #appears within the limits of the screen
                self.rect.y = random.randrange(-100,-40) #this is off the screen
                self.speedy = random.randrange(1,25)
            def update(self):
                #move downwards
                self.rect.y += self.speedy
                #deal with enemy when they get to bottom of the screen
                if self.rect.top > HEIGHT + 10:
                    self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
                    self.rect.y = random.randrange(-100,-40) #this is off the screen
                    self.speedy = random.randrange(1,25)
        text2 = 'LEVEL 5'
        draw_text2(screen,str(text2),18,WIDTH/2,30, RED)

    elif score == 500:
        class Bullet(pg.sprite.Sprite):
            def __init__(self,x,y):
                #x and y and respawn positions based on the player's position
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((10,20))
                #self.image.fill(YELLOW)
                self.image = pg.transform.scale(bullet_imgT,(80,60))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                #set respawn position to right in front of the player
                self.rect.bottom = y
                self.rect.centerx = x
                self.speedy = -5
            def update(self):
                #rect moves upwards at the speed
                self.rect.y += self.speedy
                #kill it if it moves off the top of the screen
                if self.rect.bottom < 0:
                    self.kill()
        class Mob(pg.sprite.Sprite):
            #enemy mobile object which inherits from the sprite
            def __init__(self):
                pg.sprite.Sprite.__init__(self)
                #self.image = pg.Surface((30,40))
                #self.image.fill(RED)
                self.image = pg.transform.scale(mob_img,(50,50))
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
       
                #make the enemy spawn off top of screen to appear off thescreen and then start dropping down
                self.rect.x = random.randrange(0,WIDTH - self.rect.width) #appears within the limits of the screen
                self.rect.y = random.randrange(-100,-40) #this is off the screen
                self.speedy = random.randrange(1,20)
            def update(self):
                #move downwards
                self.rect.y += self.speedy
                #deal with enemy when they get to bottom of the screen
                if self.rect.top > HEIGHT + 10:
                    self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
                    self.rect.y = random.randrange(-100,-40) #this is off the screen
                    self.speedy = random.randrange(1,20)
        text2 = 'LEVEL 6'
        draw_text2(screen,str(text2),18,WIDTH/2,30, RED)
        

    #Check to see if a mob hits the player
    hits = pg.sprite.spritecollide(player,mobs,False)
    #parameters are object to check against and group against
    #False indicates whether hit item in group should be deleted or not
   
#respawn mobs destroyed by bullets
    if hits:
        running = False
    #draw/render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text1(screen,str(score),18,WIDTH/2,10, RED)
    draw_text2(screen,str(text2),18,WIDTH/2,25, RED)
    #always do this after drawing anything
    pg.display.flip()

Username = input('Enter Username: ')
Password = input('Enter Password: ')

c.execute('''INSERT INTO Users
          VALUES (?,?,?)''', (Username, Password, score))

#terminate the game window and close everything up    
pg.quit
conn.commit()
conn.close()