import pygame
#import numpy as np
import itertools
import random
import copy
import pprint
from basicAgent import *
#from setup import *


def improvedAgent(grid, dim):
    markedMines = 0
    foundMines = 0
    KBList = []
    unvisited = list(itertools.product(range(dim), range(dim)))

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
    
    length = dim**2
    randCount = 0

    #Keep track of the border
    borderHidden = set()

    #Decision making loop
    while (length != 0):
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
        #Otherwise, we could not infer anything. So choose randomly
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

def guessAndCheck(grid, dim, borHid, KB):
    #Go through all the hidden squares that border known squares
    #These are the only squares were making an assumption makes sense  
    for (x,y) in borHid:
        for i in range(2):
            #Don't mess with the actual knowledge base
            copyKB = copy.deepcopy(KB)
            if(i == 0):
                #Assume this square is a bomb
                copyKB[(x,y)][0] = -1
                guessBomb = extendAssumption(grid, copyKB, dim)
                if(guessBomb == False):
                    #If contradiction, then we know this square must be safe
                    return 1, x, y
            else:
                #Assume this square is safe
                copyKB[(x,y)][0] = 2
                guessSafe = extendAssumption(grid, copyKB, dim)
                if(guessSafe == False):
                    #If contradiction, then we know this square must be a bomb
                    return 2, x, y

        #If no contradictions, then we cannot assume anything about this square

    #No assumptions could be successfully made with the current knowledge base
    return 0,0,0


# Essentially perform basicCheck(1 or 2), except do not actually open any squares
# Keep updating the knowledge base with the assumption until we cannot update anymore
# Return true if there are no contradictions, return false if there are
def extendAssumption(grid, KB, dim):
    conclusion = True
    while(conclusion):
        conclusion = False
        for x,y in KB.keys():
            if KB[(x,y)][0] != 1:
                continue

            KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid, KB, dim, x, y)
            

            numNeighbors = 8
            if x == 0 or x== dim-1:
                numNeighbors -=3
            if y == 0 or y == dim -1:
                numNeighbors -=3
            if numNeighbors<3: 
                numNeighbors = 3

            if KB[(x,y)][1] - KB[(x,y)][3] < 0 or numNeighbors - KB[(x,y)][1] - KB[(x,y)][2] < 0:
                #If there are more surrounding mines than the clue states or
                #If there are more safe squares than Neighbors - Clue
                #Then we hit a contradiction, our assumption does not work
                return False

            if KB[(x,y)][4] == 0:
                continue

            neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
            properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
            properNeighbors.remove((x,y))
        
            
            if KB[(x,y)][1] - KB[(x,y)][3] == KB[(x,y)][4]:
                #all hidden are mines, mark them
                for i,j in properNeighbors:
                    if KB[(i,j)][0] == 0:
                        KB[(i,j)][0] = -1
                conclusion = True
            elif numNeighbors- KB[(x,y)][1]- KB[(x,y)][2] == KB[(x,y)][4]:
                #neighbors - clues - safeNeigh == hiddenNeigh, all are safe
                conclusion = True
                for i,j in properNeighbors:
                    if KB[(i,j)][0] == 0:
                        KB[(i,j)][0] = 2

    #If we cannot update our knowledge base anymore, and there are no contradictions
    #Then our assumption is a possibly true. No information gained
    return True

#Same as checkBasic(), except this one also keeps track of the hidden squares that border revealed squares
def checkBasic2(grid, dim, unvisited, uvLen, borHid, KB, markedMines, foundMines):
    #Keep looping until the knowledge base cannot be updated by using single clues
    conclusion = True
    while(conclusion):
        conclusion = False
        for x,y in KB.keys():
            if KB[(x,y)][0] != 1:
                #No info to be revealed from non-safe squares
                continue

            KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid, KB, dim, x, y)
            if KB[(x,y)][4] == 0:
                #No info to be revealed from squares with no hidden neighbors
                continue

            numNeighbors = 8
            if x == 0 or x== dim-1:
                numNeighbors -=3
            if y == 0 or y == dim -1:
                numNeighbors -=3
            if numNeighbors<3: 
                numNeighbors = 3
            

            if KB[(x,y)][1] - KB[(x,y)][3] == KB[(x,y)][4]:
                #All these hidden neighbor squares are bombs
                
                #No longer need flagged squares on the border
                removeHiddenFromBorder(borHid, KB, dim, x, y)
                mark = markHiddenAsBombs(grid, dim, unvisited, KB, x, y)
                markedMines += mark
                uvLen -= mark
                conclusion = True
            elif numNeighbors- KB[(x,y)][1]- KB[(x,y)][2] == KB[(x,y)][4]:
                #all hidden neighbors are safe
                conclusion = True

                #Remove these neighbors from the border
                removeHiddenFromBorder(borHid, KB, dim, x, y)
                neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
                properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
                properNeighbors.remove((x,y))
                
                #Open all of these neighbors
                for i,j in properNeighbors:
                    if KB[(i,j)][0] == 0:
                        unvisited.remove((i,j))
                        uvLen -=1
                        markedMines, foundMines, uvLen = recursiveMineCheck2(grid, dim, unvisited, uvLen, borHid,KB, i, j, markedMines, foundMines)

    #We can no longer use one clue to gain information about a square
    return markedMines, foundMines, uvLen

def recursiveMineCheck2(grid, dim, unvisited, uvLen, borHid, KB, x, y, markedMines, foundMines):
    
    if KB[(x,y)][0] !=0:
        #We can't open non-hidden squares
        return markedMines, foundMines, uvLen
    clue = grid[x][y]

    #Get rid of this square from the border if it hasn't already been removed
    borHid.discard((x,y))
    if clue != -1:
        #This square is safe, update knowledge base
        KB[(x,y)][0] = 1
        KB[(x,y)][1] = clue
        KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid,KB, dim, x, y)
        
        #Add all hidden neighbors to the border since they now border a revealed square
        addBorderHidden(borHid, KB, dim, x, y)
        
        numNeighbors = 8
        if x == 0 or x== dim-1:
            numNeighbors -=3
        if y == 0 or y == dim -1:
            numNeighbors -=3
        if numNeighbors<3: 
            numNeighbors = 3
        
        
        if clue - KB[(x,y)][3] == KB[(x,y)][4]:
            #all these squares are mines
            #Remove from border and mark them
            removeHiddenFromBorder(borHid, KB, dim, x, y)
            mark = markHiddenAsBombs(None, dim, unvisited, KB, x, y)
            markedMines += mark
            uvLen -= mark
            return markedMines, foundMines, uvLen
        elif numNeighbors-clue-KB[(x,y)][2] == KB[(x,y)][4]:
            #neighbors - clues - safeNeigh == hiddenNeigh, so all are safe
            #remove them from the border since we will open them
            removeHiddenFromBorder(borHid, KB, dim, x, y)
            neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
            properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
            properNeighbors.remove((x,y))

            #Open these neighbors
            for i,j in properNeighbors:
                if KB[(i,j)][0] == 0:
                    unvisited.remove((i,j))
                    uvLen -=1
                    markedMines, foundMines, uvLen = recursiveMineCheck2(grid, dim, unvisited, uvLen, borHid, KB, i, j, markedMines, foundMines)
        else:
            #No information easily deducible, return
            return markedMines, foundMines, uvLen
    else:
        #Opened a mine. Record this incident
        foundMines +=1
        KB[(x,y)][0] = -2
        return markedMines, foundMines, uvLen
    
    #We are done with this square for now
    return markedMines, foundMines, uvLen


def removeHiddenFromBorder(borHid, KB, dim, i, j):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((i,j))

    #Check if the neighbor is hidden, remove from the border if it is
    for x,y in properNeighbors:
        if KB[(x,y)][0]== 0:
            borHid.discard((x,y))
    return None


def addBorderHidden(borHid, KB, dim, i, j):
    neighbors = list(itertools.product(range(i-1, i+2), range(j-1, j+2)))
    properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
    properNeighbors.remove((i,j))

    #Check if the neighbor is hidden, add to the border if it is
    for x,y in properNeighbors:
        if KB[(x,y)][0]== 0:
            borHid.add((x,y))
    return None

'''d = 20
b = 100

same = 0
improved = 0
worse = 0
falseP = 0
falseP2 = 0
# for i in range(1):
grid = [[ 0 , 0,  2, -1,  2,  1,  1,  2, -1, -1],
 [ 1,  1,  2, -1,  3,  2, -1,  3,  5, -1],
 [-1,  1,  2,  3, -1,  2,  2, -1,  3, -1],
 [ 1,  1,  1, -1,  2,  1,  2,  2,  3,  1],
 [ 0,  0,  1,  1,  2,  1,  2, -1,  1,  0],
 [ 0,  0,  0,  1,  3, -1,  3,  1,  1,  0],
 [ 0,  0,  0,  1, -1, -1,  3,  1,  1,  0],
 [ 1,  1,  0,  1,  2,  2,  2, -1,  1,  0],
 [-1,  2,  2,  1,  1,  0,  1,  1,  2,  1],
 [ 2, -1,  2, -1,  1,  0,  0,  0,  1, -1]]
    # grid = generateMineField(d, b)
    # mark2, num2, guesses2 = improvedAgent(grid, d)
    # if(num2 != b):
    #     falseP += 1
    #     print("Oops, missed mines or false positives")
for i in range(20):
    grid = generateMineField(d, b)
    mark, num, guesses = basicAgent(grid, d, b)
    mark2, num2, guesses2 = improvedAgent(grid, d)
    if(mark == mark2):
        same += 1
    elif( mark < mark2):
        improved += 1
    else:
        worse += 1

    if(num != b):
        falseP += 1
        print("Oops, missed mines or false positives in Basic")
    if(num2 != b):
        falseP2 += 1
        print("Oops, missed mines or false positives in Basic")

print("\n\n")
print("Improved: " + str(improved))
print("Same: " + str(same))
print("Worse: " + str(worse))
print("False Flags Basic: " + str(falseP))
print("False Flags Improved: " + str(falseP2))
'''


# d = 30
# b = 200

# same = 0
# improved = 0
# worse = 0
# falseP = 0

# for i in range(20):
#     grid = generateMineField(d, b)
#     mark, num, guesses = basicAgent(grid, d, b)
#     mark2, num2, guesses2 = improvedAgent(grid, d, b)
#     if(mark == mark2):
#         same += 1
#     elif( mark < mark2):
#         improved += 1
#     else:
#         worse += 1

#     if(num != b):
#         falseP += 1
#         print("Oops, missed mines or false positives")

# print("\n\n")
# print("Improved: " + str(improved))
# print("Same: " + str(same))
# print("Worse: " + str(worse))
# print("False Flags: " + str(falseP))
