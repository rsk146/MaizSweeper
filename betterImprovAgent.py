import pygame
#import numpy as np
import itertools
import random
import copy
import pprint
from improvAgent import *
from basicAgent import *

def improvedAgentBetter(grid, dim, numBombs):
    markedMines = 0
    foundMines = 0
    KBList = []
    unvisited = list(itertools.product(range(dim), range(dim)))


    length = dim**2

    #initialize knowledge base
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
    
    randCount = 0

    #Keep track of the border
    borderHidden = set()

    #Decision making loop
    while (markedMines + foundMines < numBombs):
        #use the current knowledge base and mark any obvious squares using 1 clue
        markedMines, foundMines, length = checkBasic2(grid, dim, unvisited, length, borderHidden, KB, markedMines, foundMines)
        if(length == 0):
            break
        
        #If we can no longer use a single clue, try to make an assumption about a border square
        #If the assumption works, then check will be non-zero
        #We should continue after a successful assumption since we need to do basic checks before assumptions before random 
        check, randX, randY = guessAndCheck(grid, dim, borderHidden, KB)
        if(check == 1):
            #randX, randY is a Safe square. Open it
            temp = foundMines
            markedMines, foundMines, length = recursiveMineCheck2(grid, dim, unvisited, length, borderHidden, KB, randX, randY, markedMines, foundMines)
            if(temp != foundMines):
                #This should never print, since our assumptions are always logic based
                print("Bad Assumption")
            continue
        elif(check == 2):
            #randX,randY is a Bomb square, mark it
            KB[(randX,randY)][0] = -1
            markedMines += 1
            unvisited.remove((randX,randY))
            length -= 1
            borderHidden.discard((randX,randY))
            continue
        #Otherwise, we could not infer anything. So choose randomly for the first guess
        #Every subsequent guess will pick a square with the smallest probability of being a bomb
        if randCount != 0:
            randX, randY = findLowestProbBomb(grid, dim, KB, length, borderHidden, markedMines, foundMines, numBombs)
            if(randX,randY == -1,-1):
                randX,randY = unvisited.pop(random.randint(0, length-1))
            else:
                unvisited.remove((randX,randY))
        else:
            randX,randY = unvisited.pop(random.randint(0, length-1))
        
        length -= 1
        randCount += 1

        #Open the random square
        markedMines, foundMines, length = recursiveMineCheck2(grid, dim, unvisited, length, borderHidden, KB, randX, randY, markedMines, foundMines)
    
   
    numMines = markedMines + foundMines
    if(not checkKB(grid, KB)):
        #If there is a contradiction in the knowledge base at the end, then we messed up
        #This should never print
        print("Marked mines do not match actual mines")
    return markedMines, numMines, randCount

def findLowestProbBomb(grid, dim, KB, length, borHid, mines, found, total):
    #Find the prob of a random square thats not on the order (worst case estimate)
    totalFoundMines = mines + found
    prob = (total - totalFoundMines)/length

    probList = []

    #Create a prob list
    for key in KB.keys():
        if(KB[key][0] == 0):
            probList.append((key, prob))
    
    probD = dict(probList)

    #Update all border hidden squares to have the highest bomb prob
    for key in borHid:
        probD[key] = calculateBombProb(grid, dim, KB, key, prob)
    
    #Get any minimum bomb prob square
    resultX, resultY = getMinProb(probD)

    return resultX, resultY

def getMinProb(probD):

    minProb = 100
    minKey = (-1,-1)
    
    #Loop through and find the key with the smallest bomb prob
    for k,v in probD.items():
        if(minProb > v):
            minProb = v
            minKey = k
    
    return minKey


    

def calculateBombProb(grid, dim, KB, key, maxProb):
    x = key[0]
    y = key[1]

    #get neighbors
    neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((x,y))
    
    max = maxProb
    for x,y in properNeighbors:
        if(KB[(x,y)][0] != 1):
            #continue if the neighbor gives no info about (x,y)
            continue

        #calculate the bomb probability based on this neighbor
        KB[(x,y)][1] = grid[x][y] 
        KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid, KB, dim, x, y)
        prob = (KB[(x,y)][1] - KB[(x,y)][3])/KB[(x,y)][4]

        #Keep track of the max bomb probability
        if (prob > max):
            max = prob

    return max