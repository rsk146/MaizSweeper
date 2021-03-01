import pygame
import numpy as np
import itertools
import random

def generateMineField(dim, numMines):
    grid = []
    for row in range(dim):
        grid.append([])
        for column in range(dim):
            grid[row].append(0)
    for i in range(numMines):
        randX, randY = (random.randint(0, dim-1), random.randint(0, dim-1))
        grid[randX][randY] = -1
    #print(grid)
    for row in range(dim):
        for col in range(dim):
            grid[row][col] = getNeighborMines(grid, row, col, dim)
    print(grid)

def getNeighborMines(grid, i, j, dim):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    countMines = 0
    for row, col in neighbors:
        if isValidNeighbor(row, col, dim):
            if grid[row][col] == -1:
                countMines+=1
    return countMines

def isValidNeighbor(x, y, dim):
    if 0 <=x <dim and 0 <= y <dim:
        return True
    return False
