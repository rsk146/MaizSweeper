import pygame
import numpy as np
import itertools
import random
#import setup
import copy
import pprint

def improvedAgent(grid, dim, numMines):
    import minesweeper as ms
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


    while (length != 0):
        #Change this function to also update some list of bordering hidden squares
        markedMines, foundMines, length = ms.checkBasic(grid, dim, unvisited, length, KB, markedMines, foundMines)
        if(length == 0):
            break
        ######################################
        #insert code to infer from our knowledge base, return some value to signify that KB has changed
        #continue; (if KB has changed)
        ######################################
        randX, randY = unvisited.pop(random.randint(0, length-1))
        length -= 1
        randCount += 1
        print("Checking " + str((randX,randY)))
        #Change this function to also update some list of bordering hidden squares
        markedMines, foundMines, length = ms.recursiveMineCheck(grid, dim, unvisited, length, KB, randX, randY, markedMines, foundMines)
    
    #pprint.pprint(KB)
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