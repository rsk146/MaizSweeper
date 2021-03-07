import pygame
import numpy as np
import itertools
import random
import setup
import copy
import pprint

def generateMineField(dim, numMines):
    grid = []
    for row in range(dim):
        grid.append([])
        for column in range(dim):
            grid[row].append(0)
    copyGrid = copy.deepcopy(grid)
    i = 0
    while i < numMines:
        randX, randY = (random.randint(0, dim-1), random.randint(0, dim-1))
        if grid[randX][randY] != -1:
            grid[randX][randY] = -1
            i+=1
    for row in range(dim):
        for col in range(dim):
            if grid[row][col] == -1: 
                continue
            grid[row][col] = getNeighborMines(grid, row, col, dim)
    print(np.matrix(grid))
    #uncomment if you want to play yourself
    #setup.manualGame(grid, dim, copyGrid)
    return grid

def getNeighborMines(grid, i, j, dim):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    #print(properNeighbors)
    countMines = 0
    for row, col in properNeighbors:
        if grid[row][col] == -1:
            countMines+=1
    return countMines
#                   -2       ,  -1       ,   0, 1   
#KB: (row,col)->(found mine/marked mine/hidden/safe, surrounding mines from clue, safe squares around it, mines around it, hidden squares around it)
def basicAgent(grid, dim, numMines):
    markedMines = 0
    foundMines = 0
    KBList = []
    for row in range(dim):
        for col in range(dim):
            hiddenNeighbors = 8
            if row == 0 or row == dim-1:
                hiddenNeighbors -=3
            if col == 0 or row == dim-1:
                hiddenNeighbors -=3
            if hiddenNeighbors < 3:
                hiddenNeighbors = 3
            KBList.append(((row,col), [0, -1, -1, -1, hiddenNeighbors]))
    KB = dict(KBList)
    #pprint.pprint(KB)
    while (markedMines + foundMines != numMines):
        randX, randY = (random.randint(0, dim-1), random.randint(0, dim-1))
        markedMines, foundMines = recursiveMineCheck(grid, dim, KB, randX, randY, markedMines, foundMines)
    
    #pprint.pprint(KB)
    print("Score: " + str(float(markedMines)/numMines))
    

def countNeighborSquares(grid, KB, dim, i, j):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    #print(neighbors)
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((i,j))
    #print(properNeighbors)
    hiddenSquares = 0
    safeSquares = 0
    bombSquares = 0
    for row, col in properNeighbors:
        #print(str(KB[(row,col)][0]))
        if KB[(row,col)][0] == 0:
            hiddenSquares+=1
        elif KB[(row,col)][0] == 1:
            safeSquares+=1
        else:
            bombSquares+=1
    #print((safeSquares, bombSquares, hiddenSquares))
    return (safeSquares, bombSquares, hiddenSquares)

def recursiveMineCheck(grid, dim, KB, x, y, markedMines, foundMines):
    revealedMines = markedMines+foundMines
    if KB[(x,y)][0] !=0:
        return markedMines, foundMines
    clue = grid[x][y]

    if clue != -1:
        KB[(x,y)][0] = 1
        KB[(x,y)][1] = clue
        KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid,KB, dim, x, y)
        #return markedMines, foundMines
        numNeighbors = 8
        if x == 0 or x== dim-1:
            numNeighbors -=3
        if y == 0 or x == dim -1:
            numNeighbors -=3
        if numNeighbors<3: 
            numNeighbors = 3
        #print((clue, revealedMines, x,y, KB[(x,y)]))
        if clue - revealedMines == KB[(x,y)][4]:
            markHiddenAsBombs(grid, dim, KB, x, y)
            markedMines += clue
            return markedMines, foundMines
        elif numNeighbors-clue-KB[(x,y)][2] == KB[(x,y)][4]:
            #print("in safe bombs func")
            neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
            properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
            properNeighbors.remove((x,y))
            for i,j in properNeighbors:
                if KB[(i,j)][0] == 0:
                    markedMines, foundMines = recursiveMineCheck(grid, dim, KB, i, j, markedMines, foundMines)
        else:
            return markedMines, foundMines
    else:
        print("Oop, ya blew up. Anyway")
        foundMines +=1
        KB[(x,y)][0] = -2
        return markedMines, foundMines
    
    return markedMines, foundMines
def markHiddenAsBombs(grid, dim, KB,i,j):
    #print("in hid bombs func")
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((i,j))
    for x,y in properNeighbors:
        if KB[(x,y)][0]== 0:
            KB[(x,y)][0] = -1
grid = generateMineField(2, 1)
basicAgent(grid, 2, 1)