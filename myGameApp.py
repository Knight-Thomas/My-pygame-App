#imports
import pygame as pg
import random

#parameters
WIDTH, HEIGHT, FPS = (800,600,30)

#define colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#sprite class
'''a sprite will be an object which inherits from the built in sprite class'''
class Player(pg.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        #constructor
        pg.sprite.Sprite.__init__(self)
        '''inheritance'''
        self.image = pg.Surface((50,50))
        '''surface gives you something to draw on'''
        self.image.fill(GREEN)
        '''useful for moving, size, position and collision'''
        self.rect = self.image.get_rect()
        '''looks at the image and gets its rect'''
        self.rect.center = (WIDTH/2, HEIGHT/2)
        '''places image in the centre'''
        self.speedx = 0
    
    def update(self):
        #move the sprite
        '''we will keep the default speed of the object to zero and only after it with a key press
        this way we avoid coding for what happens when the hey is released'''
        self.speedx = 0
        keystate = pg.key.get_pressed()
        '''returned a list of keys that are down'''
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        '''move at speed to be set by controls'''
        if self.rect.left > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

#initialise pygame contents
pg.init()
pg.mixer.init()
'''mixer is required for sound'''

#create the window
screen = pg.display.set_mode((WIDTH, HEIGHT))
'''set mode takes one thing therefore it has two brackets'''
pg.display.set_caption('My Game')
clock = pg.time.Clock()
'''handles the speed'''

class Mob(pg.sprite.Sprite):
    #enemy mobile object which inherits from the sprite
    def __init__(self):
        #constructor method
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        #make the enemy spawn off top of the screen to appear off the screen and then start dropping down
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        '''appears within the limits of the screen'''
        self.rect.y = random.randrange(-100,-40)
        '''this is off the screen'''
        self.speedy = random.randrange(1,8)
    def update(self):
        #move downwards
        self.rect.y += self.speedy
        #deal with enemy when they get to the bottom of the screen
        if self.rect.top > HEIGHT +10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            '''appears within the limits of the screen and then start dropping down'''
            self.rect.y = random.randrange(-100,-40)
            '''this is off the screen'''
            self.speedy = random.randrange(1,8)

#create a sprite group
all_sprites = pg.sprite.Group()
'''instantiate the player object and add it to the sprite group'''
mobs = pg.sprite.Group()

player = Player()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

all_sprites.add(player)
#game loop
running = True
while running:
    '''keep the game runnin at the right speed'''
    clock.tick(FPS)
    '''process input events (events)'''
    '''You want to code the ability to close the game when the user quits'''
    '''pygame will keep track of all events using an event loop'''
    for event in pg.event.get():
        '''check event for closing window'''
        if event.type == pg.QUIT:
            running = False

    #update
    all_sprites.update()
    #draw/render
    screen.fill(BLUE)
    '''always do this after drawing everything'''
    pg.display.flip()

#terminate the game window and close everythng up    
pg.quit()