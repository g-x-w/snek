import pygame as pg
import time as tt

class square (object):
    rows = 0
    width = 0

    def __init__(self, start, dir_x = 1, dir_y = 0, clr = (255,0,0)):
        pass

    def move(self, dir_x, dir_y):
        pass

    def draw(self, window, eyes = False):
        pass

class snek (object):
    body = []
    turns = {}

    def __init__(self, clr, pos):
        self.clr = clr
        self.head = square(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1

    def move (self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            
            keys = pg.key.get_pressed()
            
            for key in keys:
                if keys[pg.key.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                elif keys[pg.key.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                elif keys[pg.key.K_UP]:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                elif keys[pg.key.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        
        for i, j in enumerate(self.body):
            p = j.pos[:]
            
            if p in self.turns:
                turn = self.turns[p]
                j.move(turn[0], turn[1])
                if i == len(self.body) -1:
                    self.turns.pop(p)
            
            else:
                if ((j.dir_x == -1 and j.pos[0] <= 0) or (j.dir_x == 1 and j.pos[0] >= j.rows-1) or 
                    (j.dir_x == 1 and j.pos[1] >= j.rows-1) or (j.dir_x == -1 and j.pos[1] <= 0)):
                    terminate()
                else:
                    j.move(j.dir_x, j.dir_y)

    def reset (self, pos):
        pass

    def extend (self):
        pass

    def draw (self, window):
        for i, j in enumerate(self.body):
            if i == 0:
                j.draw(window, True)
            else:
                j.draw(window)



def draw_grid(width, rows, window):
    row_size = width//rows
    x = 0
    y = 0

    for i in range(rows):
        x += row_size
        y += row_size
        pg.draw.line(window, (255,255,255), (x,0), (x, width))
        pg.draw.line(window, (255,255,255), (0,y), (width, y))

def redraw (window):
    global rows, width, snake
    snake.draw(window)
    window.fill((0,0,0))
    draw_grid(width, rows, window)
    pg.display.update()

def terminate (window):
    pass

def main():
    global width, rows, snake
    width = 500
    rows = 10
    window = pg.display.set_mode((width, width))

    snake = snek((255,0,0), (10,10))
    goal = True
    clock = pg.time.Clock()

    while goal:
        pg.time.delay(50)
        clock.tick(10)
        redraw(window)

    pass