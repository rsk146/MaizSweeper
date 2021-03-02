import pygame
import numpy as np
import itertools
import random
import setup

def generateMineField(dim, numMines):
    grid = []
    for row in range(dim):
        grid.append([])
        for column in range(dim):
            grid[row].append(0)
    for i in range(numMines):
        randX, randY = (random.randint(0, dim-1), random.randint(0, dim-1))
        grid[randX][randY] = -1
    for row in range(dim):
        for col in range(dim):
            if grid[row][col] == -1: 
                continue
            grid[row][col] = getNeighborMines(grid, row, col, dim)
    #print(np.matrix(grid))
    copyGrid = []
    for row in range(dim):
        copyGrid.append([])
        for column in range(dim):
            copyGrid[row].append(0)
    while(1):
        setup.display(grid, dim, copyGrid)

def getNeighborMines(grid, i, j, dim):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    countMines = 0
    for row, col in properNeighbors:
        if grid[row][col] == -1:
            countMines+=1
    return countMines

generateMineField(10, 5)