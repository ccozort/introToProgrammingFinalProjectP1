# Pathfinding - Part 1
# Graphs
# KidsCanCode 2017
# using breadth first search:
'''
Until frontier is empty:
1. remove next location from frontier
2. mark location as visited
3. expand by adding location's neighbors to frontier


'''
import pygame as pg
from pygame.sprite import Sprite
from os import path

from math import floor
from math import ceil
from time import sleep
# from timers import *
# a queue like deque - each item is assigned a priority and keeps them ordered by priority.
import heapq
# need  to account for removal of items and re-indexing; re-indexing lists is very inefficient
# deque is double ended queue - allows adding to beginning and end, cannot add middle items; can popleft() or append more efficiently
from collections import deque
# q = deque()

from datetime import datetime

# Getting the current date and time
dt = datetime.now()

# getting the timestamp
ts = datetime.timestamp(dt)
vec = pg.math.Vector2

TILESIZE = 48
GRIDWIDTH = 28
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FOREST = (34, 57, 10)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
MEDGRAY = (75, 75, 75)
LIGHTGRAY = (140, 140, 140)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        # adds or removes diagonals
        # comment/uncomment this for diagonals:
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    # initial solution favors a direction moving through connnections from start to end
    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        # this solution switches front to back for connections, to switch back and forth looking for shortest path
        # commented out after adding diagonals to connections
        # if (node.x + node.y) % 2:
        #     neighbors.reverse()
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
        
# child class of grid that allows for the assignments of weights when moving from one node to another

class WeightedGrid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 0) + 10
        else:
            return self.weights.get(to_node, 0) + 14
    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
        for tile in self.weights:
            x,y = tile
            rect = pg.Rect(x * TILESIZE + 3, y * TILESIZE + 3, TILESIZE  - 3, TILESIZE - 3)
            pg.draw.rect(screen, FOREST, rect)

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

def a_star_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost + heuristic(end, vec(next))
                # add below for improved search efficiency, but less intelligent
                # priority = heuristic(end, vec(next))
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    global done
    done = True
    return path

def dijkstra_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path
  

class Mob(Sprite):
    def __init__(self,w,h,spawn_point):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.spawn_point = spawn_point
        self.pos = self.spawn_point
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.last_update = 0
        self.tick = 0
        self.frame_delay = 500
        self.path = {}
        self.trail = []
   
    def animate(self):
        now = pg.time.get_ticks()
        # print(self.tick)
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.tick += 1
            # print(self.tick)
            # print(len(self.trail[self.tick]))
        if self.tick < len(self.trail):
            self.pos = self.trail[self.tick]
        # if len(self.trail) != 0:
        #     # if len(self.steps)-1 < self.tick and self.trail[self.tick] != None:
        #     if len(self.trail)-1 < self.tick:
        #         print('in range')
        #         self.pos = self.trail[self.tick]
        #     else:
        #         self.pos = self.trail[-1]
    def update(self):
        self.rect.topleft = self.pos*TILESIZE

def path_steps(path):
    global path_length
    path_length = 0
    trail = []
    if done:
        current = start
        while current != goal:
            v = path[(current.x, current.y)]
            if v.length_squared() == 1:
                path_length += 10
            else:
                path_length += 14
            img = arrows[vec2int(v)]
            x = current.x * TILESIZE + TILESIZE / 2
            y = current.y * TILESIZE + TILESIZE / 2
            r = img.get_rect(center=(x, y))
            screen.blit(img, r)
            # find next in path
            current = current + path[vec2int(current)]
            trail.append(current)
        return(trail)
font_name = pg.font.match_font('hack')
def draw_text(text, size, color, x, y, align="topleft"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    screen.blit(text_surface, text_rect)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

def draw_icons():
    start_center = (goal.x * TILESIZE + TILESIZE / 2, goal.y * TILESIZE + TILESIZE / 2)
    screen.blit(home_img, home_img.get_rect(center=start_center))
    goal_center = (start.x * TILESIZE + TILESIZE / 2, start.y * TILESIZE + TILESIZE / 2)
    screen.blit(cross_img, cross_img.get_rect(center = goal_center))

# needed because vectors in pygame can't be used as keys in dict
def vec2int(v):
    return(int(v.x), int(v.y))

def heuristic(node1, node2):
    # manhattan distance
    return (abs(node1.x - node2.x) + abs(node1.y - node2.y))*10


icon_dir = path.join(path.dirname(__file__), 'images')

home_img = pg.image.load(path.join(icon_dir, 'home.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (TILESIZE, TILESIZE))
home_img.fill((0, 255, 0, 255), special_flags=pg.BLEND_RGBA_MULT)

cross_img = pg.image.load(path.join(icon_dir, 'cross.png')).convert_alpha()
cross_img = pg.transform.scale(cross_img, (TILESIZE, TILESIZE))
cross_img.fill((255, 0, 0, 255), special_flags=pg.BLEND_RGBA_MULT)

arrows = {}
arrow_img = pg.image.load(path.join(icon_dir, 'arrowRight.png')).convert_alpha()
arrow_img = pg.transform.scale(arrow_img, (TILESIZE,TILESIZE))

# added diagonal options
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
    arrows[dir] = pg.transform.rotate(arrow_img, vec(dir).angle_to(vec(1,0)))

all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()

# g = SquareGrid(GRIDWIDTH, GRIDHEIGHT)
g = WeightedGrid(GRIDWIDTH, GRIDHEIGHT)     

# # standard walls
# walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]
# for wall in walls:
#     g.walls.append(vec(wall))

# difficult terrain
terrain = [(11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (16, 8), (15, 8), (14, 8), (13, 8), (12, 8), (11, 8), (10, 8), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (12, 11), (13, 11), (14, 11), (12, 5), (13, 5), (14, 5), (11, 5), (15, 5), (12, 4), (13, 4), (14, 4)]
# terrain = []
for tile in terrain:
    g.weights[tile] = 15
start = vec(0,0)
goal = vec(0, 0)
# path = breadth_first_search(g, goal, start)
# path = dijkstra_search(g, goal, start)
search_type = a_star_search
path = search_type(g, goal, start)
running = True
# trail = []
current = start
path_length = 0

while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            
            if event.key == pg.K_p:
                print('mpos ' + str(vec(pg.mouse.get_pos()) // TILESIZE))
                # print('frontier ' + str(frontier.nodes))
                # print('path ' + str(path))
                print('path key for current ' + str(path[(int(current.x), int(current.y))]))
                print('mob steps ' + str(mob.steps))
                print('start ' + str(start))
                print('current ' + str(current))
                print('goal ' + str(goal))
                print('mob position ' + str(mob.pos))
                print('trail ' + str(trail))
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_m:
                # dump the wall list for saving
                print([(int(loc.x), int(loc.y)) for loc in g.walls])
            if event.key == pg.K_LCTRL:
                path = search_type(g, goal, start)

                # print(mpos)
            if event.key == pg.K_SPACE:
                current = start
                trail = []
                if search_type == a_star_search:
                    search_type = dijkstra_search
                else:
                    search_type = a_star_search
                path = search_type(g, goal, start)
                mob.tick = 0
        if event.type == pg.MOUSEBUTTONDOWN:
            current = start
            # trail = []
            mpos = vec(pg.mouse.get_pos()) // TILESIZE
            if event.button == 1:
                if mpos in g.walls:
                    g.walls.remove(mpos)
                else:
                    g.walls.append(mpos)
            if event.button == 2:
                start = mpos
                current = start
                mob = Mob(TILESIZE, TILESIZE, start)
                mob.tick = 0
                # path = search_type(g, goal, start)
                # mob.trail = path_steps(path)
                mob.path = search_type(g, goal, start)
                mob.trail = path_steps(mob.path)
                mobs.add(mob)
                all_sprites.add(mob)
                # print(mob.trail)
            if event.button == 3:
                goal = mpos
                # current = start
                # mob = Mob(TILESIZE, TILESIZE, start)
                # path = search_type(g, goal, start)
                # mob.trail = path_steps(path)
                for mob in mobs:
                    x = len(mob.trail) - mob.tick
                    mob.trail = path_steps(search_type(g, goal, vec(mob.rect.topleft)))
                    if x < len(mob.trail):
                        mob.tick = len(mob.trail) - x
                    
                # mobs.add(mob)
                # all_sprites.add(mob)
                # print(mob.trail)
                    
            # apply diijkstra search when clicked
            # path = search_type(g, goal, start)
              
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    # fill explored area using path info
    # for node in path:
    #     x, y = node
    #     rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
    #     pg.draw.rect(screen, MEDGRAY, rect)
    
    # draw path from start to goal
    # path_steps(path)

    for m in mobs:
        # m.trail = trail
        m.animate()
        for node in m.path:
            x, y = node
            rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pg.draw.rect(screen, MEDGRAY, rect)
    draw_grid()
    g.draw()
    mobs.update()
    all_sprites.update()
    
    draw_text(search_type.__name__, 30, GREEN, WIDTH - 10, HEIGHT - 10, align="bottomright")
    draw_text('Path length:{}'.format(path_length), 30, GREEN, WIDTH - 10, HEIGHT - 30, align="bottomright")
    # for i in trail:
    #     r = pg.Rect(i.x * TILESIZE + 9, i.y * TILESIZE + 9, TILESIZE - 14, TILESIZE - 14)
    #     pg.draw.rect(screen, YELLOW, r)

    
    all_sprites.draw(screen)
    draw_icons()
    pg.display.flip()
