import pygame
import numpy as np
import itertools
import random
#import setup
import copy
import pprint

def generateMineField(dim, numMines):
    #Create square field that is dim by dim
    grid = []
    for row in range(dim):
        grid.append([])
        for column in range(dim):
            grid[row].append(0)
    
    i = 0
    
    #randomly place mines until numMines have been placed
    while i < numMines:
        randX, randY = (random.randint(0, dim-1), random.randint(0, dim-1))
        if grid[randX][randY] != -1:
            grid[randX][randY] = -1
            i+=1
    
    #Mark the number of mines surrounding each non-mine square
    for row in range(dim):
        for col in range(dim):
            if grid[row][col] == -1: 
                continue
            grid[row][col] = getNeighborMines(grid, row, col, dim)
    

    #uncomment if you want to play yourself
    #setup.manualGame(grid, dim, copyGrid)
    return grid


def getNeighborMines(grid, i, j, dim):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    
    countMines = 0
    for row, col in properNeighbors:
        if grid[row][col] == -1:
            countMines+=1
    return countMines

#KB: (row,col)-> (Status, Clue, knownSafeNeighbors, knownMineNeighbors, hiddenNeighbors)
# 
# Status =              Found mine (-2) / Marked mine (-1) / Hidden(0) / Safe(1)
# Clue =                Number of mines that should surround (row,col)
# knownSafeNeighbors =  Number of safe squares around (row,col)
# knownMineNeighbors =  Number of detonated or flagged squares around (row,col)
# hiddenNeighbors =     Number of unknown squares around (row,col))

def basicAgent(grid, dim):
    markedMines = 0
    foundMines = 0
    KBList = []
    unvisited = list(itertools.product(range(dim), range(dim)))

    #Initialize our knowledge base
    for row in range(dim):
        for col in range(dim):
            hiddenNeighbors = 8
            if row == 0 or row == dim-1:
                hiddenNeighbors -=3
            if col == 0 or col == dim-1:
                hiddenNeighbors -=3
            if hiddenNeighbors < 3:
                hiddenNeighbors = 3
            KBList.append(((row,col), [0, -1, -1, -1, hiddenNeighbors]))
    KB = dict(KBList)
    

    length = dim**2
    randCount = 0

    #Decision making loop
    while (length != 0):
        #Use the current knowledge base to see if we can deduce something with only one clue
        markedMines, foundMines, length = checkBasic(grid, dim, unvisited, length, KB, markedMines, foundMines)
        if(length == 0):
            break
        
        #If we can no longer deduce anything, just randomly choose a square
        randX, randY = unvisited.pop(random.randint(0, length-1))
        length -= 1
        randCount += 1
        
        #Check our random square until we have to use our knowledge base again
        markedMines, foundMines, length = recursiveMineCheck(grid, dim, unvisited, length, KB, randX, randY, markedMines, foundMines)
    
    #Game is over, print score
    #print("Score: " + str(float(markedMines)/numMines))
    #print("Guesses: " + str(randCount))
    numMines = markedMines + foundMines
    return markedMines, numMines, randCount
    
def checkBasic(grid, dim, unvisited, uvLen, KB, markedMines, foundMines):
    conclusion = True

    #Continously check through our knowledge base and keep markign stuff until we cant anymore
    while(conclusion):
        conclusion = False
        for x,y in KB.keys():
            #If the square is not a safe square, then continue since we cant get any info
            if KB[(x,y)][0] != 1:
                continue

            #Update our knowledge of this square. If there are no hidden neighbors, continue since we can't get any info
            KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid, KB, dim, x, y)
            if KB[(x,y)][4] == 0:
                continue

            #Calculate the number of neighbors around the square (needed for borders)
            numNeighbors = 8
            if x == 0 or x== dim-1:
                numNeighbors -=3
            if y == 0 or y == dim -1:
                numNeighbors -=3
            if numNeighbors<3: 
                numNeighbors = 3
            
            
            if KB[(x,y)][1] - KB[(x,y)][3] == KB[(x,y)][4]:
                #Clue - knownMineNeighbors == hiddenNeighbors => All hidden are mines 
                mark = markHiddenAsBombs(grid, dim, unvisited, KB, x, y)
                markedMines += mark
                uvLen -= mark
                conclusion = True
            elif numNeighbors- KB[(x,y)][1]- KB[(x,y)][2] == KB[(x,y)][4]:
                #neighbors - clues - safeNeigh == hiddenNeigh ==> All hidden are safe
                conclusion = True
                neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
                properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
                properNeighbors.remove((x,y))

                #Since we know the neighbors are all safe, we can open all of these neighbors
                for i,j in properNeighbors:
                    if KB[(i,j)][0] == 0:
                        unvisited.remove((i,j))
                        uvLen -=1
                        markedMines, foundMines, uvLen = recursiveMineCheck(grid, dim, unvisited, uvLen, KB, i, j, markedMines, foundMines)

    #If we return here, this means that we cannot deduce anything using a single clue
    return markedMines, foundMines, uvLen


def countNeighborSquares(grid, KB, dim, i, j):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((i,j))
    
    hiddenSquares = 0
    safeSquares = 0
    bombSquares = 0

    #Use knowledge base to count hidden, safe, and bombs
    for row, col in properNeighbors:
        if KB[(row,col)][0] == 0:
            hiddenSquares+=1
        elif KB[(row,col)][0] == 1 or KB[(row,col)][0] == 2:
            safeSquares+=1
        else:
            bombSquares+=1
    
    return (safeSquares, bombSquares, hiddenSquares)

def recursiveMineCheck(grid, dim, unvisited, uvLen, KB, x, y, markedMines, foundMines):
    #If we try to open an already known square, then just return
    if KB[(x,y)][0] !=0:
        return markedMines, foundMines, uvLen

    #Open the square
    clue = grid[x][y]

    
    if clue != -1:
        #If this square is not a bomb, update our knowledge base
        KB[(x,y)][0] = 1
        KB[(x,y)][1] = clue
        KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid,KB, dim, x, y)
        
        #Get number of neighbors
        numNeighbors = 8
        if x == 0 or x== dim-1:
            numNeighbors -=3
        if y == 0 or y == dim -1:
            numNeighbors -=3
        if numNeighbors<3: 
            numNeighbors = 3
        
        if clue - KB[(x,y)][3] == KB[(x,y)][4]:
            #Clue - knownMineNeighbors == hiddenNeighbors => All hidden are mines
            mark = markHiddenAsBombs(None, dim, unvisited, KB, x, y)
            markedMines += mark
            uvLen -= mark
            return markedMines, foundMines, uvLen
        elif numNeighbors-clue-KB[(x,y)][2] == KB[(x,y)][4]:
            #neighbors - clues - safeNeigh == hiddenNeigh ==> All hidden are safe
            neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
            properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
            properNeighbors.remove((x,y))

            #Since we know the neighbors are all safe, we can open all of these neighbors
            for i,j in properNeighbors:
                if KB[(i,j)][0] == 0:
                    unvisited.remove((i,j))
                    uvLen -=1
                    markedMines, foundMines, uvLen = recursiveMineCheck(grid, dim, unvisited, uvLen, KB, i, j, markedMines, foundMines)
        else:
            #Nothing can be deduced from this square
            return markedMines, foundMines, uvLen
    else:
        #We opened a bomb. Mark that and update database
        foundMines +=1
        KB[(x,y)][0] = -2
        return markedMines, foundMines, uvLen
    
    #We are done with this square for now
    return markedMines, foundMines, uvLen

def markHiddenAsBombs(grid, dim, unvisited, KB,i,j):
    markedBombs = 0
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((i,j))

    #Go through all hidden neighbors and mark them as bomb in the database
    for x,y in properNeighbors:
        if KB[(x,y)][0]== 0:
            KB[(x,y)][0] = -1
            markedBombs += 1
            unvisited.remove((x,y))
    return markedBombs

#Make sure that the knowledge base doesn't contradict the actual grid
#Returns false on contradiction. Returns true if there are none
def checkKB(grid, KB):
    for (x,y) in KB.keys():
        if(KB[(x,y)][0] == -1 or KB[(x,y)][0] == -2):
            if(grid[x][y] != -1):
                #If we marked something as a bomb, but it wasnt actually
                return False
        elif(KB[(x,y)][0] == 1 and grid[x][y] == -1):
            #If we marked something is safe, but it was actually a bomb
            return False
    return True    