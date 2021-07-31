import math
import pygame as pg
import funcs

pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 25)


class vector:
    def __init__(self, mag, angle):
        self.mag = mag
        self.angle = angle


class bounce:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.bounce = 2

        self.rad = 15
        self.mult = 1
    def draw(self, surface):
        pg.draw.circle(surface, (0,0,255), (self.x, self.y), self.rad)

class wall:
    def __init__(self, s,e):
        self.start = s
        self.end = e
        self.bounce = 1.6
    def draw(self, surface):
        pg.draw.line(surface, (0,0,0), (self.start), (self.end), 3)


class flipper:
    def __init__(self, x,y, walllst):
        self.x = x
        self.y = y
        self.length = 50
        self.idleA = 2.35619
        self.flippedA = 3.49066
        self.endF = ((math.cos(self.flippedA)*self.length)+self.x, (math.sin(self.flippedA)*self.length)+self.y)
        self.endI = ((math.cos(self.idleA)*self.length)+self.x, (math.sin(self.idleA)*self.length)+self.y)

        self.bouncePos = (0,0)

        self.w = wall((self.x,self.y), self.endI)
        walllst.append(self.w)
        
        
        self.flipped = False
        self.key = pg.K_SLASH
        self.prev = False
    def draw(self, surface):
        if self.flipped:
            pg.draw.line(surface, (0,0,0), (self.x, self.y), self.endF, 3)
        else:
            ex = math.cos(self.idleA) * self.length + self.x
            ey = math.sin(self.idleA) * self.length + self.y
            pg.draw.line(surface, (0,0,0), (self.x, self.y), (ex,ey), 3)
            


class puck:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vel = vector(0,0)
    def draw(self, surface):
        pg.draw.circle(surface, (255,255,255), (int(self.x),int(self.y)), 5)
    def phys(self, g):
        if self.vel.mag > 10:
            self.vel.mag = 10

        self.vel = funcs.vectadd(self.vel, g)

        self.x += math.cos(self.vel.angle) * self.vel.mag
        self.y += math.sin(self.vel.angle) * self.vel.mag


class button:
    def __init__(self, x,y,w,h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.colour = (0,0,0)
        self.fill = 0#full width, 0 = solid
        self.text = ""
    
    def draw(self, surface):
        pg.draw.rect(surface, self.colour, (self.x, self.y, self.width, self.height), self.fill)
        text = myfont.render(self.text, False, (0,0,0))
        surface.blit(text, (self.x, self.y))

    def detect(self, mx,my,m1):
        if mx > self.x and mx < self.x + self.width and my > self.y and my < self.y + self.height and m1:
            return 1
        return 0