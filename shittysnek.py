import math as m
import random as rd
import pygame as pg 
import tkinter as tk
from tkinter import messagebox

global width, rows
width = 240
rows = 10
AI = True

class cube(object):
    width = width
    rows = rows
    def __init__(self,start,dirnx=1,dirny=0, color=(0, 255, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pg.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pg.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pg.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    AI = AI
    width = width
    rows = rows

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self, snack_loc):
        if self.AI:
            decision = A_Star_Decider(snack_loc, self, self.width)
            # print("Direction:", decision, "\n")

            if decision == 1:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
            elif decision == 2: 
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif decision == 3:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif decision == 4:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        else:
            for event in pg.event.get():
                if event.type == quit:
                    quit()

                keys = pg.key.get_pressed()

                for key in keys:
                    if keys[pg.K_LEFT] or keys[pg.K_a]:
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pg.K_UP] or keys[pg.K_w]:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pg.K_DOWN] or keys[pg.K_s]:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if ((c.dirnx == -1 and c.pos[0] <= 0) or (c.dirnx == 1 and c.pos[0] >= c.rows-1) or 
                    (c.dirny == 1 and c.pos[1] >= c.rows-1) or (c.dirny == -1 and c.pos[1] <= 0)):
                    terminate()
                else: c.move(c.dirnx,c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def A_Star_Decider (snack_loc, s, width):
    global rows

    L_block = (s.body[0].pos[0]-1, s.body[0].pos[1])
    R_block = (s.body[0].pos[0]+1, s.body[0].pos[1])
    U_block = (s.body[0].pos[0], s.body[0].pos[1]-1)
    D_block = (s.body[0].pos[0], s.body[0].pos[1]+1)

    L = euc_dist(L_block, snack_loc)
    R = euc_dist(R_block, snack_loc)
    U = euc_dist(U_block, snack_loc)
    D = euc_dist(D_block, snack_loc)
    
    distances = [L, R, U, D]
    options = [L_block, R_block, U_block, D_block]

    # print("Options (LRUD):", options)

    distances, options = zip(*sorted(zip(distances, options)))
    distances = list(distances)
    options = list(options)
    
    illegal = list(map(lambda z: z.pos, s.body[1:]))

    for i in range(rows):
        illegal.append((i, -1))     #append -1 row
        illegal.append((i, rows))       #append bottom row
        illegal.append((-1, i))     #append -1 column     
        illegal.append((rows, i))       #append rightmost column

    # print("ILLEGAL:", illegal)
    # print("DISTANCES:", distances)
    # print("OPTIONS:", options)

    allowable = []
    for i in range(len(options)):
        if options[i] in illegal:
            pass
        else:
            allowable.append(i)
    
    # print("ALLOWED:", allowable)

    while len(allowable) > 0:
        try:
            if options[allowable[0]] == L_block:
                test = second_vision(L_block)
                # print("TEST:", test)
                case = 0
                for i in range(len(test)):
                    if test[i] in illegal:
                        case += 1
                    else:
                        pass
                if case > 2:
                    allowable.remove(allowable[0])
                else:
                    return 1

            elif options[allowable[0]] == R_block:
                test = second_vision(R_block)
                # print("TEST:", test)
                case = 0
                for i in range(len(test)):
                    if test[i] in illegal:
                        case += 1
                    else:
                        pass
                if case > 2:
                    allowable.remove(allowable[0])
                else:
                    return 2
                
            elif options[allowable[0]] == U_block:
                test = second_vision(U_block)
                # print("TEST:", test)
                case = 0
                for i in range(len(test)):
                    if test[i] in illegal:
                        case += 1
                    else:
                        pass
                if case > 2:
                    allowable.remove(allowable[0])
                else:
                    return 3

            elif options[allowable[0]] == D_block:
                test = second_vision(D_block)
                # print("TEST:", test)
                case = 0
                for i in range(len(test)):
                    if test[i] in illegal:
                        case += 1
                    else:
                        pass
                if case > 2:
                    allowable.remove(allowable[0])
                else:
                    return 4

            else:
                print("ALLOWABLE ERROR")

        except Exception:
            terminate()

def second_vision(square_tuple):
    out = ((square_tuple[0]-1, square_tuple[1]),
        (square_tuple[0]+1, square_tuple[1]),
        (square_tuple[0], square_tuple[1]-1),
        (square_tuple[0], square_tuple[1]+1)) #LRUD format
    return out

def euc_dist (tup1, tup2):
    out = ((tup2[0] - tup1[0])**2 + (tup2[1] - tup1[1])**2)**(0.5)
    return out

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pg.draw.line(surface, (255,255,255), (x,0),(x,w))
        pg.draw.line(surface, (255,255,255), (0,y),(w,y))
        
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pg.display.update()

def goal(rows, item):

    positions = item.body

    while True:
        x = rd.randrange(rows)
        y = rd.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def terminate ():
    print('{},'.format(len(s.body) -1))
    message_box('Game Over!', 'You scored {} points! Press any key to play again...'.format(len(s.body)-1))
    s.reset((0,0))
    quit()

def main():
    global s, snack, speed
    s = snake((0,255,0), (rows//2, rows//2))
    snack = cube(goal(rows, s), color=(255,0,0))
    speed = 40 # from 1 (painfully slow) to 1000 (impossibly fast)    

    win = pg.display.set_mode((width, width))
    flag = True

    clock = pg.time.Clock()
    
    while flag:
        pg.time.delay(1)
        clock.tick(speed)
        s.move(snack.pos)

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(goal(rows, s), color=(255, 0, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in map(lambda z:z.pos,s.body[x+1:]):
                # body_pos = list(map(lambda z: z.pos, s.body[1:]))
                # print("Final:", body_pos)
                terminate()

        redrawWindow(win)

main()