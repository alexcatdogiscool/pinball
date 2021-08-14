from numpy.lib.twodim_base import _trilu_indices_form_dispatcher
import pygame as pg
import random
import math
import numpy as np
import objs
import funcs




width = 500
height = 700

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
sky = (80, 147, 215)

screen = pg.display.set_mode((width, height))
pg.display.set_caption('swagball.txt')
screen.fill(black)
pg.display.flip()

escreen = pg.display.set_mode((width, height))
pg.display.set_caption('swagball.txt')
escreen.fill(black)
pg.display.flip()

pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 30)


ball = objs.puck()

walls = []
bouncers = []
flippers = []
f = objs.flipper(310, 570, walls)
f.bouncePos = (310-30, 570-7)
flippers.append(f)
f = objs.flipper(180, 570, walls)
f.bouncePos = (180+30, 570-7)
f.key = pg.K_z
f.idleA = (f.idleA + math.pi)*-1
f.flippedA = (f.flippedA + math.pi)*-1
f.endF = ((math.cos(f.flippedA)*f.length)+f.x, (math.sin(f.flippedA)*f.length)+f.y)
f.endI = ((math.cos(f.idleA)*f.length)+f.x, (math.sin(f.idleA)*f.length)+f.y)
flippers.append(f)


mapsB = objs.button(425,0,75,50)
mapsB.text = "Maps"
mapsB.colour = (255,255,255)

delBut = objs.button(350,670, 150, 30)
delBut.text = "Delete Mode"
delBut.colour = (200,55,55)
mapDel = False
delPres = False
editBut = objs.button(0,670,150,30)
editBut.text = "Edit Map"
editBut.colour = (75, 232, 58)
mapEditMode = False
mapEd = False




G = objs.vector(0.0195, math.pi/2)

clock = pg.time.Clock()

points = 0


mapNum = 0
editing = False
selecting = True
playing = False
running = True
while running:
    clock.tick(120)
    keys = pg.key.get_pressed()
    mx,my = pg.mouse.get_pos()
    m1, m3, m2 = pg.mouse.get_pressed()
    

    if not selecting and not editing:
    
        for f in flippers:
            f.flipped = keys[f.key]
            f.draw(screen)
            if f.flipped and not f.prev:
                d = funcs.norm(ball.x-f.bouncePos[0], ball.y-f.bouncePos[1])
                if d < 20 + ball.rad:
                    bv = objs.vector(random.uniform(3,6), -math.pi/2+random.uniform(-math.pi/4, math.pi/4))
                    ball.vel.mag = 0
                    ball.vel = funcs.vectadd(ball.vel, bv)
                    ball.y = 550
            f.prev = f.flipped
            if f.flipped:
                f.w.end = f.endF
            else:
                f.w.end = f.endI

        
        for b in bouncers:
            b.draw(screen)
            d = funcs.norm(b.x-ball.x, b.y-ball.y)
            if d < b.rad + ball.rad:
                angle2 = math.atan2(ball.y-b.y, ball.x-b.x)
                bv = objs.vector(ball.vel.mag * b.bounce, angle2)
                ball.vel = funcs.vectadd(ball.vel, bv)
                ball.x += math.cos(angle2) * 2
                ball.y += math.sin(angle2) * 2
                points += 25

        for w in walls:
            w.draw(screen)
            d = abs(funcs.linedst(w, ball))
            if d < 1 + ball.rad:
                lineA = math.atan2(w.start[1]-w.end[1], w.start[0]-w.end[0])
                a = lineA - math.pi/2
                temp = ball.vel.angle - lineA
                vt = (math.sin(temp) * ball.vel.mag)
                bv = objs.vector(w.bounce * vt, a)
                ball.vel = funcs.vectadd(ball.vel, bv)
                for i in range(2):
                    ball.phys(objs.vector(0,0))
                if playing:
                    points += 5

        ball.phys(G)
        ball.draw(screen)

        if ball.y > 630 and playing:
            playing = False
            if points > hiScore:
                for f in flippers:
                    f.w.start = (0,0)
                    f.w.end = (0,0)
                funcs.updateMap(mapNum, walls, bouncers, points)
                for f in flippers:
                    f.w.start = (f.x, f.y)
                w,b,f, hiScore = funcs.loadMap(mapNum)
                points = 0
            ball.vel = objs.vector(0,0)
            ball.x = 470
            ball.y = 630




        text = myfont.render(str(points), False, (0,0,0))
        screen.blit(text, (0,0))

        text = myfont.render('Hi: ' + str(hiScore), False, (0,0,0))
        screen.blit(text, (200,0))

        if not playing:
            textsurface = myfont.render('Game Over', False, (200, 50, 50))
            screen.blit(textsurface,(180,350))


        if keys[pg.K_r] and not playing:
            ball.x = 470
            ball.y = 630
            ball.vel.angle = -math.pi/2
            ball.vel.mag = random.uniform(4.8,6)
            playing = True
            points = 0
            

        mapsB.draw(screen)
        if mapsB.detect(mx,my,m1):
            buttons = []
            selecting = True

    if mapDel:
        delBut.text = "Select Map"
    else:
        delBut.text = "Delete Map"

    if selecting:
        buttons, newMapB = funcs.displayPrev(screen, (0,0,0))
        if mapDel:
            buttons, newMapB = funcs.displayPrev(screen, (200,55,55))
        if mapEditMode:
            buttons, newMapB = funcs.displayPrev(screen, (75, 232, 58))
            
        
        for b in buttons:
            b.draw(screen)
        delBut.draw(screen)
        delPres = delBut.detect(mx,my, m1)
        if delPres and not delButPre:
            mapDel = not mapDel
        editBut.draw(screen)
        mapEd = editBut.detect(mx,my,m1)
        if mapEd and not mapEdPre:
            mapEditMode = not mapEditMode
        i = -1
        for b in buttons:
            i += 1
            if b.detect(mx,my,m1) and mapEditMode and not m1Pre:
                editing = True
                selecting = False
                saveButton = objs.button(385,10, 115,40)
                saveButton.text = "Save Map"
                saveButton.colour = (75, 232, 58)
                wallSel = objs.wall((10,50), (40,10))
                wallSelButton = objs.button(10, 10, 40,40)
                wallSelButton.fill = 1
                bounceSel = objs.bounce(75,30)
                bounceSelButton = objs.button(60, 15, 30,30)
                bounceSelButton.fill = 1
                selWall = False
                selBounce = False
                wallPressPre = wallSelButton.detect(mx,my,m1)
                bouncePressPre = bounceSelButton.detect(mx,my,m1)
                Ewalls, Ebouncers, flippers, s = funcs.loadMap(i)
                del Ewalls[-1]
                del Ewalls[-1]
            if b.detect(mx,my,m1) and mapDel and not m1Pre:
                funcs.deleteMap(i)
            if b.detect(mx,my,m1) and not mapDel and not m1Pre:
                selecting = False
                walls, bouncers, flippers, hiScore = funcs.loadMap(i)
                mapNum = i
                ball.x = 470
                ball.y = 630
                ball.vel = objs.vector(0,0)
        newMapB.draw(screen)
        tmpE = newMapB.detect(mx,my,m1)
        if tmpE and not m1Pre:
            editing = tmpE
            selecting = not tmpE
        if editing:
            saveButton = objs.button(385,10, 115,40)
            saveButton.text = "Save Map"
            saveButton.colour = (75, 232, 58)
            wallSel = objs.wall((10,50), (40,10))
            wallSelButton = objs.button(10, 10, 40,40)
            wallSelButton.fill = 1
            bounceSel = objs.bounce(75,30)
            bounceSelButton = objs.button(60, 15, 30,30)
            bounceSelButton.fill = 1
            selWall = False
            selBounce = False
            wallPressPre = wallSelButton.detect(mx,my,m1)
            bouncePressPre = bounceSelButton.detect(mx,my,m1)
            if not mapEditMode:
                Ebouncers = []
                Ewalls = []


    if editing:
        pg.draw.circle(screen, (255,255,255), (470, 630), ball.rad)

        for f in flippers:
            f.draw(screen)
        for b in Ebouncers:
            b.draw(screen)
        for w in Ewalls:
            w.draw(screen)

        saveButton.draw(screen)

        if saveButton.detect(mx,my,m1):
            funcs.saveMap(Ewalls, Ebouncers, 0)
            editing = False
            selecting = True

        wallSel.draw(screen)
        bounceSel.draw(screen)
        wallSelButton.draw(screen)
        bounceSelButton.draw(screen)
        wallPress = wallSelButton.detect(mx,my,m1)
        bouncePress = bounceSelButton.detect(mx,my,m1)

        if selBounce:
            tmpBounce.x = mx
            tmpBounce.y = my
            tmpBounce.draw(screen)
            if m1 and not m1Pre:
                Ebouncers.append(tmpBounce)
                tmpBounce = objs.bounce(mx,my)

        if selWall:
            tmpWall.draw(screen)
            if ending:
                dst = 1000
                for w in Ewalls:
                    tmx, tmy = pg.mouse.get_pos()
                    tmpDS = funcs.norm(tmx-w.start[0], tmy-w.start[1])
                    tmpDE = funcs.norm(tmx-w.end[0], tmy-w.end[1])
                    tmpD = min(tmpDS, tmpDE)
                    if tmpD < dst:
                        dst = tmpD
                        if tmpDS < tmpDE:
                            mx, my = w.start
                        else:
                            mx, my = w.end
                if dst > 10:
                    mx, my = pg.mouse.get_pos()
                tmpWall.end = (mx,my)
                if m1 and not m1Pre:
                    Ewalls.append(tmpWall)
                    tmpWall = objs.wall((0,0), (0,0))
                    #selWall = False
            if m1 and not m1Pre and not ending:
                dst = 1000
                for w in Ewalls:
                    tmx, tmy = pg.mouse.get_pos()
                    tmpDS = funcs.norm(tmx-w.start[0], tmy-w.start[1])
                    tmpDE = funcs.norm(tmx-w.end[0], tmy-w.end[1])
                    tmpD = min(tmpDS, tmpDE)
                    if tmpD < dst:
                        dst = tmpD
                        if tmpDS < tmpDE:
                            mx, my = w.start
                        else:
                            mx, my = w.end
                if dst > 10:
                    mx, my = pg.mouse.get_pos()
                tmpWall.start = (mx,my)
                ending = True
            if ending and tmpWall.start == (0,0):
                ending = False
            


        if wallPress and not wallPressPre:
            selBounce = False
            if len(Ebouncers) > 0:
                del Ebouncers[-1]
            selWall = not selWall
            if selWall:
                tmpWall = objs.wall((0,0), (0,0))
                ending = False
        if bouncePress and not bouncePressPre:
            selWall = False
            selBounce = not selBounce
            if selBounce:
                tmpBounce = objs.bounce(0,0)

        wallPressPre = wallSelButton.detect(mx,my,m1)
        bouncePressPre = bounceSelButton.detect(mx,my,m1)
        if m2 and not m2Pre:
            i = -1
            for b in Ebouncers:
                i += 1
                d = funcs.norm(mx-b.x, my-b.y)
                if d < b.rad:
                    del Ebouncers[i]
                    break
            i = -1
            for w in Ewalls:
                i += 1
                d = funcs.linedst(w, objs.point(mx,my))
                if d < 5:
                    del Ewalls[i]
                    break

                




    m1Pre = m1
    m2Pre = m2
    mapEdPre = mapEd
    delButPre = delPres
    sPre = keys[pg.K_s]
    pg.display.flip()
    escreen.fill(sky)
    screen.fill(sky)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            running == False
