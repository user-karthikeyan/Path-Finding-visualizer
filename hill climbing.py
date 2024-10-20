import pygame
from time import sleep
from threading import *
from collections import defaultdict
from pygame.locals import *
from heapq import *

START = 1
END = 2
BLOCK = 3
VISITED = 4
INQUEUE = 5
PATH = 6
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (60, 255, 60)
BLUE = (39, 223, 214)
ORANGE_LIGHT = (240, 141, 65)
ORANGE_DARK = (255, 80, 10)
VIOLET = (178, 67, 190)

COLORS = [WHITE, BLUE, GREEN, BLACK, ORANGE_LIGHT, ORANGE_DARK, VIOLET]


class Grid:
    def __init__(self, rows, columns, display):
        self.rows, self.columns = rows, columns
        self.w, self.h = width // self.columns, height // self.rows
        self.display = display
        
        self.grid = [[0] * self.columns for _ in range(self.rows)]
        self.states = {0, 1, 2, 3}
        self.start = self.end = None

    def clear(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid[i][j] = 0
        self.states = {0, 1, 2, 3}
    
    def draw(self):

        self.drawBoxes()
        
        for x in range(self.w, width + 1, self.w):
            pygame.draw.line(self.display, BLACK, [x, 0], [x, height])

        for y in range(self.h, height + 1, self.h):
            pygame.draw.line(self.display, BLACK, [0, y], [width, y])
    
    def drawBoxes(self):
        for i in range(self.rows):
            for j in range(self.columns):
                pygame.draw.rect(self.display, COLORS[self.grid[i][j]], (j * self.w, i * self.h, self.w, self.h))
    
    def FlipColor(self, position):
        y, x = position[0] // self.w, position[1] // self.h
        
        self.states.add(self.grid[x][y])
        self.grid[x][y] = (self.grid[x][y] + 1) % 4

        if self.grid[x][y] == START:
            if self.grid[x][y] in self.states:
                self.states.remove(self.grid[x][y])
                self.start = (x, y)
            else:
                self.grid[x][y] = (self.grid[x][y] + 1) % 4
        
        
        if self.grid[x][y] == END:
            if self.grid[x][y] in self.states:
                self.states.remove(self.grid[x][y])
                self.end = (x, y)
            else:
                self.grid[x][y] = (self.grid[x][y] + 1) % 4


    def get_args(self):
        return self.start, self.end, self.grid, self.rows, self.columns
            
def color(grid, color, x, y):
    if grid[x][y] != START and grid[x][y] != END:
        grid[x][y] = color

def find_path(start, end, grid, m, n):
    neighbours = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    g_score = defaultdict(lambda : float("inf"))
    parent = dict()
    h_score = lambda x, y : abs(end[0] - x) + abs(end[1] - y)
    g_score[start[0], start[1]] = 0

    path = []
    current = (0, 0, start)

    while current:
        current_g_score, f_score, (x, y) = current
        color(grid, VISITED, x, y)
        sleep(0.2)

        if (x, y) == end:
            current = (x, y)
            while current:
                color(grid, PATH, *current)
                path.insert(0, current)
                current = parent.get(current, None)
                sleep(0.2)
            break
            
        successor = None

        for i, j in neighbours:
            new_x, new_y = x + i, y + j

            if not (0 <= new_x < m and 0 <= new_y < n):
                continue

            if grid[new_x][new_y] == BLOCK:
                continue

            if grid[new_x][new_y] != VISITED:
                current_successor = (current_g_score + 1, current_g_score + 1 + h_score(new_x, new_y), (new_x, new_y))
                if successor is None:
                    successor = current_successor
                else:
                    successor = min(current_successor, successor, key = lambda val:val[1])
        
        if successor is not None:
            parent[successor[2][0], successor[2][1]] = x, y 

        current = successor
    return path




pygame.init()
run = True
width = 600
height = 600

screen = pygame.display.set_mode([width, height])
grid = Grid(20, 20, screen)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            grid.FlipColor(event.pos)
        elif event.type == KEYDOWN and event.key == K_SPACE and len(grid.states) == 2:
            simulation = Thread(target = find_path, args = grid.get_args())
            simulation.start()
        elif event.type == KEYDOWN and event.key == K_c:
            grid.clear()

    screen.fill((255, 255, 255))
    grid.draw()
    pygame.display.update()
    
pygame.quit()
    