import math
import objs
import numpy as np
import pygame as pg



def norm(a,b):
    return math.sqrt(a*a + b*b)


def vectadd(v1,v2):
    v1x = math.cos(v1.angle) * v1.mag
    v1y = math.sin(v1.angle) * v1.mag
    v2x = math.cos(v2.angle) * v2.mag
    v2y = math.sin(v2.angle) * v2.mag
    
    vx = v1x + v2x
    vy = v1y + v2y
    vt = objs.vector(norm(vx,vy), math.atan2(vy,vx))
    return vt


def linedst(line, point):
    p3 = (point.x, point.y)
    d1 = np.cross(np.asarray(line.end)-np.asarray(line.start), np.asarray(line.start)-p3)/norm(line.start[0]-line.end[0], line.start[1]-line.end[1])
    d2 = norm(point.x-line.start[0], point.y-line.start[1])
    d3 = norm(point.x-line.end[0], point.y-line.end[1])
    l = norm(line.start[0]-line.end[0], line.start[1]-line.end[1])
    if max(d2,d3) > l:
        return min(d2,d3)
    return d1


def saveMap(walls, bouncers, score):
    f = open('map.txt', 'a')# [(sx,sy,ex,ey(wall2(wall3(etc[(x,y(bouncer2(etc
    f.write(str(score))
    f.write('[')
    for w in walls:
        f.write('(')
        f.write(str(int(w.start[0])) + ',' + str(int(w.start[1])) + ',' + str(int(w.end[0])) + ',' + str(int(w.end[1])))
    f.write('[')
    for b in bouncers:
        f.write('(')
        f.write(str(int(b.x)) + ',' + str((b.y)))
    f.write("+")
    f.close()


def loadMap(mapSel):
    walllst = []
    bouncerlst = []
    f = open('map.txt', 'r')
    data = f.read().split("+")[mapSel]

    objects = data.split("[")
    score = int(objects[0])
    walls = objects[1].split("(")
    del walls[0]
    bouncers = objects[2].split("(")
    del bouncers[0]

    for w in walls:
        pos = w.split(",")
        start = (int(pos[0]), int(pos[1]))
        end = (int(pos[2]), int(pos[3]))
        line = objs.wall(start, end)
        walllst.append(line)

    for b in bouncers:
        pos = b.split(",")
        boun = objs.bounce(int(pos[0]), int(pos[1]))
        bouncerlst.append(boun)


    flippers = []
    f = objs.flipper(310, 570, walllst)
    f.bouncePos = (310-30, 570-7)
    flippers.append(f)
    f = objs.flipper(180, 570, walllst)
    f.bouncePos = (180+30, 570-7)
    f.key = pg.K_z
    f.idleA = (f.idleA + math.pi)*-1
    f.flippedA = (f.flippedA + math.pi)*-1
    f.endF = ((math.cos(f.flippedA)*f.length)+f.x, (math.sin(f.flippedA)*f.length)+f.y)
    f.endI = ((math.cos(f.idleA)*f.length)+f.x, (math.sin(f.idleA)*f.length)+f.y)
    flippers.append(f)

    return walllst, bouncerlst, flippers, score


def updateMap(mapNum, walls, bouncers, score):
    f = open('map.txt', 'r')
    data = f.read().split("+")
    
    f = []
    f.append(str(score))
    f.append('[')
    for w in walls:
        f.append('(')
        f.append(str(int(w.start[0])) + ',' + str(int(w.start[1])) + ',' + str(int(w.end[0])) + ',' + str(int(w.end[1])))
    f.append('[')
    for b in bouncers:
        f.append('(')
        f.append(str(int(b.x)) + ',' + str((b.y)))
    #f.append("+")
    newMap = ''.join(f)

    data[mapNum] = newMap

    newD = '+'.join(data)
    f = open('map.txt', 'w')
    f.write(newD)
    f.close()


def displayPrev(surface, buttonColour):
    f = open('map.txt')
    mapNum = (f.read().split("+"))
    del mapNum[0]
    mapNum = len(mapNum)

    buttons = []

    ymult = 0

    for i in range(mapNum):
        walls, bouncers, flippers, points = loadMap(i)
        ymult = (i // 4)
        b = objs.button((i-(4*ymult))*100, (ymult * 140), 100, 130)
        b.fill = 1
        b.colour = buttonColour
        buttons.append(b)
        for w in walls:
            w.start = (w.start[0] // 5 + ((i-(4*ymult))*100), w.start[1] // 5 + (ymult * 140))
            w.end = (w.end[0] // 5 + ((i-(4*ymult))*100), w.end[1] // 5 + (ymult * 140))
            w.draw(surface)
        for b in bouncers:
            b.x = b.x // 5 + ((i-(4*ymult))*100)
            b.y = b.y // 5 + (ymult * 140)
            b.rad //= 5
            b.draw(surface)

    ymult = mapNum // 4
    newMapB = objs.button(((mapNum-(4*ymult))*100), (ymult * 140), 100, 130)
    newMapB.fill = 3
    newMapB.text = "NewMap"
    return buttons, newMapB

    
def deleteMap(mapNum):
    f = open('map.txt', 'r')
    data = f.read().split("+")
    del data[mapNum]
    d = "+"
    data = d.join(data)
    f = open('map.txt', 'w')
    f.write(data)


