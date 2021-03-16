import pygame
#import numpy as np
import itertools
import random
#import setup
import copy
import pprint
from minesweeper import *


def improvedAgent(grid, dim, numMines):
    markedMines = 0
    foundMines = 0
    KBList = []
    unvisited = list(itertools.product(range(dim), range(dim)))

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
    length = dim**2
    randCount = 0

    borderHidden = set()

    while (length != 0):
        #Change this function to also update some list of bordering hidden squares
        markedMines, foundMines, length = checkBasic2(grid, dim, unvisited, length, borderHidden, KB, markedMines, foundMines)
        if(length == 0):
            break
        ######################################
        #insert code to infer from our knowledge base, return some value to signify that KB has changed
        #continue; (if KB has changed)
        ######################################
        check, randX, randY = guessAndCheck(dim, borderHidden, KB)
        if(check == 1):
            #Safe square
            recursiveMineCheck2(grid, dim, unvisited, length, borderHidden, KB, randX, randY, markedMines, foundMines)
            continue
        elif(check == 2):
            #Bomb square
            KB[(randX,randY)][0] = -1
            markedMines += 1
            unvisited.remove((randX,randY))
            borderHidden.discard((randX,randY))
            continue
        #Otherwise, we could not infer anything
        
        randX, randY = unvisited.pop(random.randint(0, length-1))
        length -= 1
        randCount += 1
        print("Checking " + str((randX,randY)))
        #Change this function to also update some list of bordering hidden squares
        markedMines, foundMines, length = recursiveMineCheck2(grid, dim, unvisited, length, borderHidden, KB, randX, randY, markedMines, foundMines)
    
    #pprint.pprint(KB)
    print(len(borderHidden))
    print("Score: " + str(float(markedMines)/numMines))
    print("Guesses: " + str(randCount))
    return markedMines, numMines, randCount


    #Some function that makes inferences
    #
    #LOOP 1
    # Pick next square in borderHiddenSquares
    #LOOP 2
    #copies the current knowledge base
    #Then infers pickedSquare is a bomb
    #Extends the knowledge of the copied KB based on the assumption
    #Checks for any contradiction in the copied KB
    #If no contradiction, then this is inconclusive. Go back to LOOP 2 but see what happens if the square is known safe
    #If still no contradiction, then go back to LOOP 1 and pick the next square
def guessAndCheck(dim, borHid, KB):


    return 0,0,0


def checkBasic2(grid, dim, unvisited, uvLen, borHid, KB, markedMines, foundMines):
    conclusion = True
    while(conclusion):
        conclusion = False
        for x,y in KB.keys():
            if KB[(x,y)][0] != 1:
                continue

            KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid, KB, dim, x, y)
            if KB[(x,y)][4] == 0:
                continue

            numNeighbors = 8
            if x == 0 or x== dim-1:
                numNeighbors -=3
            if y == 0 or x == dim -1:
                numNeighbors -=3
            if numNeighbors<3: 
                numNeighbors = 3
            #print((clue, revealedMines, x,y, KB[(x,y)]))
            if KB[(x,y)][1] - KB[(x,y)][3] == KB[(x,y)][4]:
                removeHiddenFromBorder(borHid, KB, dim, x, y)
                mark = markHiddenAsBombs(grid, dim, unvisited, KB, x, y)
                markedMines += mark
                uvLen -= mark
                conclusion = True
            elif numNeighbors- KB[(x,y)][1]- KB[(x,y)][2] == KB[(x,y)][4]:
                #neighbors - clues - safeNeigh == hiddenNeigh
                #print("in safe bombs func")
                conclusion = True
                removeHiddenFromBorder(borHid, KB, dim, x, y)
                neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
                properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
                properNeighbors.remove((x,y))
                for i,j in properNeighbors:
                    if KB[(i,j)][0] == 0:
                        unvisited.remove((i,j))
                        uvLen -=1
                        markedMines, foundMines, uvLen = recursiveMineCheck2(grid, dim, unvisited, uvLen, borHid,KB, i, j, markedMines, foundMines)

    return markedMines, foundMines, uvLen

def recursiveMineCheck2(grid, dim, unvisited, uvLen, borHid, KB, x, y, markedMines, foundMines):
    #revealedMines = markedMines+foundMines
    #print(len(borHid))
    if KB[(x,y)][0] !=0:
        return markedMines, foundMines, uvLen
    clue = grid[x][y]

    borHid.discard((x,y))
    if clue != -1:
        KB[(x,y)][0] = 1
        KB[(x,y)][1] = clue
        KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid,KB, dim, x, y)
        addBorderHidden(borHid, KB, dim, x, y)
        #return markedMines, foundMines
        numNeighbors = 8
        if x == 0 or x== dim-1:
            numNeighbors -=3
        if y == 0 or x == dim -1:
            numNeighbors -=3
        if numNeighbors<3: 
            numNeighbors = 3
        #print((clue, revealedMines, x,y, KB[(x,y)]))
        if clue - KB[(x,y)][3] == KB[(x,y)][4]:
            removeHiddenFromBorder(borHid, KB, dim, x, y)
            mark = markHiddenAsBombs(None, dim, unvisited, KB, x, y)
            markedMines += mark
            uvLen -= mark
            return markedMines, foundMines, uvLen
        elif numNeighbors-clue-KB[(x,y)][2] == KB[(x,y)][4]:
            #neighbors - clues - safeNeigh == hiddenNeigh
            #print("in safe bombs func")
            removeHiddenFromBorder(borHid, KB, dim, x, y)
            neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
            properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
            properNeighbors.remove((x,y))
            for i,j in properNeighbors:
                if KB[(i,j)][0] == 0:
                    unvisited.remove((i,j))
                    uvLen -=1
                    markedMines, foundMines, uvLen = recursiveMineCheck2(grid, dim, unvisited, uvLen, borHid, KB, i, j, markedMines, foundMines)
        else:
            return markedMines, foundMines, uvLen
    else:
        print("Oop, ya blew up. Anyway")
        foundMines +=1
        KB[(x,y)][0] = -2
        return markedMines, foundMines, uvLen
    
    return markedMines, foundMines, uvLen

def removeHiddenFromBorder(borHid, KB, dim, i, j):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((i,j))
    for x,y in properNeighbors:
        if KB[(x,y)][0]== 0:
            borHid.discard((x,y))
    return None

def addBorderHidden(borHid, KB, dim, i, j):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((i,j))
    for x,y in properNeighbors:
        if KB[(x,y)][0]== 0:
            borHid.add((x,y))
    return None

d = 20
b = 10

grid = generateMineField(d, b)
mark, num, guesses = improvedAgent(grid, d, b)

if(num != b):
    print("Oops, missed mines or false positives")