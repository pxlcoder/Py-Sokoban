import pygame, sys, os
from pygame.locals import *
from random import randint

fullscreen = False

f = open(os.path.join("data","level.txt"), "r")

levels = [[] for x in xrange(15)]
checksolved = [False for x in xrange(15)]

loc = 0
lines = 0

for line in f:
    levels[loc].append(line.strip().split(","))
    lines += 1
    if lines % 10 == 0:
        loc += 1

f.close()

levelnumber = 0
moves = 0

m = levels[levelnumber]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("sprites","pusher.png"))
        self.rect = self.image.get_rect()
    def update(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
    def push(self,blocks,walls,goals,moves,direction):
        x = 0
        y = 0

        if direction == "RIGHT":
            x = 30
            y = 0
        elif direction == "LEFT":
            x = -30
            y = 0
        elif direction == "UP":
            x = 0
            y = -30
        elif direction == "DOWN":
            x = 0
            y = 30

        check = self.rect.move(x,y)
        for b in blocks:
            if check.colliderect(b):
                checkb = b.rect.move(x,y)
                if not any(checkb.colliderect(w) for w in walls):
                    if not any(checkb.colliderect(c) for c in blocks if b != c):
                        b.rect.move_ip(x,y)
                        b.changestate(goals)
                break

        if not any(check.colliderect(w) for w in walls):
            try:
                if not any(checkb.colliderect(w) for w in walls):
                    if not any(checkb.colliderect(c) for c in blocks if b != c):
                        p.rect.move_ip(x,y)
            except NameError:
                p.rect.move_ip(x,y)

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("sprites","wall.png"))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("sprites","boxon.png"))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.solved = None
    def changestate(self,goals):
        if any(self.rect.colliderect(g.rect) for g in goals):
           self.image = pygame.image.load(os.path.join("sprites","boxon.png"))
           self.solved = True
        else:
            self.image = pygame.image.load(os.path.join("sprites","boxoff.png"))
            self.solved = False

class Goal(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("sprites","target.png"))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


class Floor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("sprites","floor.png"))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

window = pygame.display.set_mode((345,270))
pygame.display.set_caption("Sokoban")

checkmark = pygame.image.load(os.path.join("sprites","truesolved.png"))
checkmark = pygame.transform.scale(checkmark, (100,100))

xmark = pygame.image.load(os.path.join("sprites","notsolved.png"))
xmark = pygame.transform.scale(xmark, (100,100))

p = Player()
blocks = pygame.sprite.Group()
walls = pygame.sprite.Group()
goals = pygame.sprite.Group()
floors = pygame.sprite.Group()

for x in xrange(8):
        for y in xrange(9):
            f = Floor(x*30,y*30)
            floors.add(f)

pygame.font.init()

textbase = pygame.font.SysFont("myriad pro",15)

def setup(new=False):
    global levels, m, levelnumber

    if new == True:
        if levelnumber + 1 > len(levels)-1:
            levelnumber = 0
        else:
            levelnumber += 1
        m = levels[levelnumber]

    blocks.empty()
    walls.empty()
    goals.empty()

    window.fill((0,0,0))

    for x in xrange(8):
        for y in xrange(9):
            if m[y][x] == "#":
                walls.add(Wall(x*30,y*30))
            elif m[y][x] == "@":
                p.update(x*30, y*30)
                window.blit(p.image,(x*30, y*30))
            elif m[y][x] == "$":
                blocks.add(Block(x*30,y*30))
            elif m[y][x] == ".":
                goals.add(Goal(x*30,y*30))
            elif m[y][x] == "*":
                goals.add(Goal(x*30,y*30))
                blocks.add(Block(x*30,y*30))


    for b in blocks:
        b.changestate(goals)

    pygame.display.update()

def generalupdate():
    window.blit(p.image,p.rect)
    blocks.draw(window)

    movestext = textbase.render("Moves:" + str(moves), True, (255,255,255))
    levelstext = textbase.render("Level: " + str(levelnumber+1), True, (255,255,255))
    titletext = textbase.render("SOKOBAN", True, (255,255,255))
    arrowinfo = textbase.render("Move: Arrow Keys", True, (255,255,255))
    resetinfo = textbase.render("Reset: [R]", True, (255,255,255))
    skipinfo = textbase.render("Skip: [SPACE]", True, (255,255,255))
    ginfo = textbase.render("Give Up: [G]", True, (255,255,255))
    finfo = textbase.render("Fullscreen: [F]", True, (255,255,255))

    window.blit(movestext, (window.get_width()-movestext.get_width()-2,window.get_height()-movestext.get_height()))
    window.blit(levelstext, (window.get_width()-levelstext.get_width()-2,window.get_height()-movestext.get_height()-levelstext.get_height()-5))
    window.blit(titletext, (window.get_width()-titletext.get_width()-titletext.get_width()/3-5,20))
    window.blit(arrowinfo, (window.get_width()-arrowinfo.get_width()-5,50))
    window.blit(resetinfo, (window.get_width()-arrowinfo.get_width()-5,70))
    window.blit(skipinfo, (window.get_width()-arrowinfo.get_width()-5,90))
    window.blit(ginfo, (window.get_width()-arrowinfo.get_width()-5,110))
    window.blit(finfo, (window.get_width()-arrowinfo.get_width()-5,130))

    if checksolved[levelnumber] == True:
        window.blit(checkmark, (window.get_width()-checkmark.get_width()-4,window.get_height()-checkmark.get_height()-30))
    else:
        window.blit(xmark, (window.get_width()-xmark.get_width()-2,window.get_height()-xmark.get_height()-30))

    pygame.display.update()

setup()

while True:

    window.fill((0,0,0))

    floors.draw(window)
    walls.draw(window)
    goals.draw(window)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                p.push(blocks, walls, goals, moves, "LEFT")
                moves += 1
            elif event.key == K_RIGHT:
                p.push(blocks, walls, goals, moves, "RIGHT")
                moves += 1
            elif event.key == K_UP:
                p.push(blocks, walls, goals, moves, "UP")
                moves += 1
            elif event.key == K_DOWN:
                p.push(blocks, walls, goals, moves, "DOWN")
                moves += 1
            elif event.key == K_SPACE:
                setup(True)
            elif event.key == K_r:
                moves += 1
                setup()
            elif event.key == K_f:
                if fullscreen == False:
                    window = pygame.display.set_mode((345,270), FULLSCREEN)
                    fullscreen = True
                else:
                    window = pygame.display.set_mode((345,270))
                    fullscreen = False
            elif event.key == K_g:
                moves += 1000
                checksolved[levelnumber] = True
                generalupdate()
                pygame.time.delay(1000)
                setup(True)


    if all(b.solved for b in blocks):
        checksolved[levelnumber] = True
        generalupdate()
        pygame.time.delay(1000)
        setup(True)

    if all(checksolved):
        print "You took", moves, "moves to finish the game."
        pygame.quit()
        sys.exit()

    generalupdate()
