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
        # self.connections determines the directions a node can "look".  To the right, left, down, up in this case. 
        self.connections = [vec(1,0), vec(-1,0), vec(0,1), vec(0,-1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height
    
    def passable(self, node):
        return node not in self.walls
    
    def find_neighbors(self, node):
        # dynamic iteration
        #  adds 'node' to 'connection' through each iteration
        neighbors = [node + connection for connection in self.connections]

        # Filter an array and and return a new array with only values from the function/method in the first argument
        # The function passed as an argument must return true or false
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        print(list(neighbors))
        return neighbors

g = SquareGrid(5,4)
g.walls = [vec(2,1), vec(2,2)]
g.find_neighbors(vec(0,0))
g.find_neighbors(vec(3,2))


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