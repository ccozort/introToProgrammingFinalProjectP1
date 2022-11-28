'''
overview of the thing 

'''

'''
SOURCES:
https://github.com/kidscancode/pygame_tutorials/blob/master/examples/pathfinding/part1.py

'''

# import libraries

# built in

# installed modules or libraries
import pygame as pg
vec = pg.math.Vector2

# created modules or libraries
from settings import *
import sprites

# global variables

# utilities

# draw grid with tile spacing
def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))
        print(y)

# ;lkasjdf;lkasjdf

# main code body
pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1,0), vec(0,1), vec(0,1), vec(0, -1)]

    def in_bounds(self, node):

    def find_neighbors(self, node):
        # dynamic iteration
        #  adds 'node' to 'connection' through each iteration
        neighbors = [node + connection for connection in self.connections]
        filter(function or None, neighbors)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)
    draw_grid()


    pg.display.flip()