import pygame, random

from pygame.locals import *
pygame.init()

WIDTH, HEIGHT = 800, 900
ground_scroll = 0
scroll_speed = 2
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pony Escape")
background_image=pygame.image.load("bg.png")
ground_image=pygame.image.load("ground.png")
flying=False
gameover=False
gap=150
pipefrequency=1500 #milisecond
lastpipe=pygame.time.get_ticks()-pipefrequency

class Pony(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(3):
            img=pygame.image.load(f"horse{i+1}.png") # loads images in order with numbering
            self.images.append(img) # puts each image to the list
        self.image=self.images[self.index] # record of current image
        self.rect=self.image.get_rect()
        self.velocity=0
    def update(self):
        print(self.velocity)
        if flying:
            self.velocity += 0.5 # make the pony gradually fall down
            if self.velocity > 8:
                self.velocity=8
            if self.rect.bottom<700:
                self.rect.y+=self.velocity
        if gameover==False:
            if pygame.mouse.get_pressed()[0]==True:
                self.velocity=-10 # if mouse is pressed, pony goes up
            self.counter+=1
            flapdown=5
            if self.counter>flapdown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images):
                    self.index=0
            self.image=self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pipe.png")
        self.rect=self.image.get_rect()
        if position==1:
            self.image=pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft=[x, y]
        elif position==-1:
            self.rect.topleft=[x, y+gap]
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()

ponygroup=pygame.sprite.Group()
pony1=Pony(100, HEIGHT/2)
ponygroup.add(pony1)
pipegroup=pygame.sprite.Group()

run = True
while run:
    screen.blit(background_image, (0, 0))
    ponygroup.draw(screen)
    pipegroup.draw(screen)
    ponygroup.update()
    screen.blit(ground_image, (ground_scroll, 700))

    if pony1.rect.bottom >= 700:
        gameover = True
    if gameover == False:
        print(pygame.time.get_ticks())
        timenow = pygame.time.get_ticks()
        if timenow - lastpipe > pipefrequency:
            pipeheight = random.randint(200, 600)
            bottompipe = Pipe(WIDTH, pipeheight, -1)
            toppipe = Pipe(WIDTH, pipeheight, 1)
            pipegroup.add(bottompipe)
            pipegroup.add(toppipe)
            lastpipe = timenow
        pipegroup.update()
        ground_scroll -= scroll_speed
        if ground_scroll <= -100:
            ground_scroll = 0

    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            pygame.quit()
            run = False
        if i.type == pygame.MOUSEBUTTONDOWN and not flying and gameover == False:
            flying=True

    pygame.display.update()
pygame.quit()