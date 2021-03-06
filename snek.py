import random as rd
import pygame as pg 
import tkinter as tk
from tkinter import messagebox

class cube(object):

    def __init__(self, start, dirnx=1, dirny=0, color=(0, 255, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = width//rows
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

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self, snack_loc):
        if AI: # AI turned on
                decision = A_Star_Decider(snack_loc, self, width)

                if decision == 0: #LEFT
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
                elif decision == 1: #RIGHT
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif decision == 2: #UP
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif decision == 3: #DOWN
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]     

        else: # Human player
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
                if ((c.dirnx == -1 and c.pos[0] <= 0) or (c.dirnx == 1 and c.pos[0] >= rows-1) or 
                    (c.dirny == 1 and c.pos[1] >= rows-1) or (c.dirny == -1 and c.pos[1] <= 0)):
                    print("wall terminate")
                    terminate(0)
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

global width, rows, s, speed, timeout, AI
width = 600 # width of gameplay screen
rows = 40 # However many rows & columns you want
s = snake((0, 255, 0), (2, 2)) # (R,G,B)(starting x position, starting y position)
speed = 10 # from 1 (painfully slow) to 1000 (impossibly fast) 
timeout = 100 # However many cycles you want
AI = True # True or False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

illegal_walls = []
Lboundary = []
Rboundary = []
Uboundary = []
Dboundary = []
Lboundary2 = []
Rboundary2 = []
Uboundary2 = []
Dboundary2 = []

for i in range(rows):
    illegal_walls.append((i, -1))     #append -1 row
    illegal_walls.append((i, rows))       #append bottom row
    illegal_walls.append((-1, i))     #append -1 column     
    illegal_walls.append((rows, i))       #append rightmost column

    Uboundary.append((i, 0))
    Dboundary.append((i, rows-1))
    Lboundary.append((0, i))
    Rboundary.append((rows - 1, i))
    
    Uboundary2.append((i, 1))
    Dboundary2.append((i, rows-2))
    Lboundary2.append((1, i))
    Rboundary2.append((rows - 2, i))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


def A_Star_Decider (snack_loc, s, width):

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

    distances, options = zip(*sorted(zip(distances, options)))
    distances = list(distances)
    options = list(options)
    
    illegal_body = list(map(lambda z: z.pos, s.body[:]))

    allowable = []
    for i in range(len(options)):
        if options[i] in illegal_body or options[i] in illegal_walls:
            pass
        else:
            allowable.append(i)
    
    direction  = []
    for i in range(len(allowable)):
        if options[allowable[i]] == L_block:
            if len(allowable) == 1 or second_analysis(L_block, illegal_body, illegal_walls) == 1:
                direction.append(0)
            else:
                pass

        elif options[allowable[i]] == R_block:
            if len(allowable) == 1 or second_analysis(R_block, illegal_body, illegal_walls) == 1:
                direction.append(1)
            else:
                pass
            
        elif options[allowable[i]] == U_block:
            if len(allowable) == 1 or second_analysis(U_block, illegal_body, illegal_walls) == 1:
                direction.append(2)
            else:
                pass

        elif options[allowable[i]] == D_block:
            if len(allowable) == 1 or second_analysis(D_block, illegal_body, illegal_walls) == 1:
                direction.append(3)
            else:
                pass

    direction_final = []
    for n in range(len(direction)):
        boundary_count = 0
        if direction[n] == 0:
            if L_block in Lboundary:
                for i in range(len(Lboundary2)):
                    if Lboundary2 in illegal_body:
                        boundary_count += 1
                    else:
                        pass
                if 2*(boundary_count - 1) < len(illegal_body) and boundary_count == len(Lboundary):
                    pass
                else:
                    direction_final.append(direction[n])
            else:
                direction_final.append(direction[n])
        elif direction[n] == 1:
            if R_block in Rboundary:
                for i in range(len(Rboundary2)):
                    if Rboundary2 in illegal_body:
                        boundary_count += 1
                    else:
                        pass
                if 2*(boundary_count - 1) < len(illegal_body) and boundary_count == len(Rboundary):
                    pass
                else:
                    direction_final.append(direction[n])
            else:
                direction_final.append(direction[n])
        elif direction[n] == 2:
            if U_block in Uboundary:
                for i in range(len(Uboundary2)):
                    if Uboundary2 in illegal_body:
                        boundary_count += 1
                    else:
                        pass
                if 2*(boundary_count - 1) < len(illegal_body) and boundary_count == len(Uboundary):
                    pass
                else:
                    direction_final.append(direction[n])
            else:
                direction_final.append(direction[n])
        elif direction[n] == 3:
            if D_block in Dboundary:
                for i in range(len(Dboundary2)):
                    if Dboundary2 in illegal_body:
                        boundary_count += 1
                    else:
                        pass
                if 2*(boundary_count - 1) < len(illegal_body) and boundary_count == len(Dboundary):
                    pass
                else:
                    direction_final.append(direction[n])
            else:
                direction_final.append(direction[n])
            
    if len(direction_final) < 1:
        terminate(0)
    else:
        return direction_final[0]

def second_vision(square_tuple):
    out = ((square_tuple[0]-1, square_tuple[1]),
        (square_tuple[0]+1, square_tuple[1]),
        (square_tuple[0], square_tuple[1]-1),
        (square_tuple[0], square_tuple[1]+1)) #LRUD format
    return out

def second_analysis(block, body, walls):
    test = second_vision(block)
    second_body = body[0:len(body)-2]
    case = 0

    for i in range(len(test)):
        if test[i] in second_body or test[i] in walls:
            case += 1
        else:
            pass
        continue
    if case > 3:
        return 0

    else:
        return 1

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
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
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

def terminate (type):
    s.body[-1].color = (0, 0, 255) ### color tail block blue
    redrawWindow(win)
    if len(s.body) > 20:
        print('Score: {}'.format(len(s.body) - 1))
    if type == 0:
        message_box('Game Over!', 'You scored {} points! \nAnd then ran into something \nPress ENTER to close this window...'.format(len(s.body)))
        s.reset((0,0))
    elif type == 1:
        message_box('Game Over!', 'You scored {} points! \nAnd then went too long without eating and starved :( \nPress ENTER to close this window...'.format(len(s.body)))
        s.reset((0,0))
    quit()

def win_game():
    print('{},'.format(len(s.body) -1))
    message_box('You Won!', 'You scored the max {} points and won the game! Press any key to play again...'.format(len(s.body)))
    s.reset((0,0))
    quit()

def game_start(): 
    global snack, win
    snack = cube(goal(rows, s), color=(255,0,0))
    win = pg.display.set_mode((width, width))
    flag = True
    cycle_number = 0
    clock = pg.time.Clock()
    
    while flag:
        pg.time.delay(1)
        clock.tick(speed)
        s.move(snack.pos)

        if s.body[0].pos == snack.pos and len(s.body) != rows**2:
            s.addCube()
            snack = cube(goal(rows, s), color=(255, 0, 0))
            cycle_number = 0
        elif s.body[0].pos == snack.pos and len(s.body) == rows**2:
            win_game()

        cycle_number += 1
        # print("Score: {}\t Cycle number: {}\t Cycle limit: {}".format(len(s.body), cycle_number, timeout), flush=True)
        body = []
        
        for x in range(len(s.body)):
            body.append(s.body[x].pos)
        body.remove(body[0])

        if s.head.pos in body:
            terminate(0)
        elif cycle_number > timeout:
            terminate(1)

        redrawWindow(win)
        
game_start()