import pygame
import sys
from enum import Enum

#maybe just used for keeping track for myself
class Status(Enum):
    BOMB = -1
    CLEAR = 0
    
pygame.init()
size = [800,800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MineSweeper")
clock = pygame.time.Clock()

height, width, margin = (800/dim-4, 800/dim -4, 4)

def playMinesweeper(grid):
    for event in pygame.event.get():
        if event.type =- pygame.QUIT:
            sys.exit(0)


