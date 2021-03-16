import pygame
import sys
from enum import Enum
import time
import copy
#maybe just used for keeping track for myself
class Status(Enum):
    BOMB = -1
    CLEAR = 0
    
WHITE = (255, 255, 255) #Unseen
BLACK = (0,0,0)         #Bomb 
L_BLUE = (102, 255, 255)#Zero
BLUE = (0, 0, 255)      #One 
RED = (255, 0, 0)       #Two 
GREEN = (0, 100, 0)     #Three
L_GREEN = (0, 255, 0)   #Four
YELLOW = (255, 255, 0)  #Five 
PURPLE = (255,0,255)    #Six
PINK = (255, 192, 203)  #Seven
ORANGE = (255, 128, 0) #Eight

pygame.init()
size = [800,800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MineSweeper")
clock = pygame.time.Clock()
dim = 10
height, width, margin = (800/dim-4, 800/dim -4, 4)
font = pygame.font.SysFont('arial', 40) #this line takes so longfor some reason


def manualGame(grid, dim, copyGrid):
    
    #print(copyGrid)
    for row in range(dim):
        for col in range(dim):
            color = WHITE
            pygame.draw.rect(screen, color, [(margin + width) * col + margin,
                                                (margin+ height) * row + margin,
                                                width, height])
    pygame.display.update()
    pygame.display.flip()
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                i = int(pos[0]//(width +margin))
                j = int(pos[1]//(height+margin))
                #print((j,i))
                if 0<= i < dim and 0<=j < dim:
                    copyGrid[j][i] = 1
        for row in range(dim):
            for col in range(dim):
                color = WHITE
                if copyGrid[col][row] == 1:
                    #print((col,row))
                    # if grid[row][col] == -1:
                    #     color = BLACK
                    # elif grid[row][col] ==0:
                    #     color = L_BLUE
                    # elif grid[row][col] ==1:
                    #     color = BLUE
                    # elif grid[row][col] ==2:
                    #     color = RED
                    # elif grid[row][col] ==3:
                    #     color = GREEN
                    # elif grid[row][col] ==4:
                    #     color = L_GREEN
                    # elif grid[row][col] ==5:
                    #     color = YELLOW
                    # elif grid[row][col] ==6:
                    #     color = PURPLE
                    # elif grid[row][col] ==7:
                    #     color = PINK
                    # elif grid[row][col] ==8:
                    #     color = ORANGE
                    text = font.render(str(grid[col][row]), True, (0,0,0))
                    #print(grid[row][col])
                    rect = text.get_rect()
                    #print(((margin+ height) * row + margin, (margin + width) * col + margin))
                    #time.sleep(1)
                    rect = pygame.Rect.move(rect, (margin+ height) * row + margin, (margin + width) * col + margin)
                    screen.blit(text, rect)
                    #print("in loop")
                    pygame.display.update()
                # else:
                #     pygame.draw.rect(screen, color, [(margin + width) * col + margin,
                #                                     (margin+ height) * row + margin,
                #                                     width, height])
        pygame.display.update()
        pygame.display.flip()
   
   
   
   
    '''Draw a number
    font=pygame.font.SysFont('arial', 40)
    text=font.render(str(grid[row][col]), True, (0, 0, 0))
    rect=text.get_rect()
    rect = pygame.Rect.move(rect, 20, 20)
    screen.fill((255,255,255))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.display.flip()
    time.sleep(1)'''