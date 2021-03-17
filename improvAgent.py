import pygame
#import numpy as np
import itertools
import random
import copy
import pprint
from minesweeper import *
#from setup import *
import matplotlib.pyplot as plt


def improvedAgent(grid, dim):
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
        #displayGrid(grid, dim, KB)
        #input()
        #Change this function to also update some list of bordering hidden squares
        markedMines, foundMines, length = checkBasic2(grid, dim, unvisited, length, borderHidden, KB, markedMines, foundMines)
        if(length == 0):
            break
        ######################################
        #insert code to infer from our knowledge base, return some value to signify that KB has changed
        #continue; (if KB has changed)
        ######################################
        check, randX, randY = guessAndCheck(grid, dim, borderHidden, KB)
        if(check == 1):
            #Safe square
            temp = foundMines
            markedMines, foundMines, length = recursiveMineCheck2(grid, dim, unvisited, length, borderHidden, KB, randX, randY, markedMines, foundMines)
            if(temp != foundMines):
                print("Bad Assumption")
                input()
            continue
        elif(check == 2):
            #Bomb square
            KB[(randX,randY)][0] = -1
            markedMines += 1
            unvisited.remove((randX,randY))
            length -= 1
            borderHidden.discard((randX,randY))
            continue
        #Otherwise, we could not infer anything

        # if(randCount == 0):
        #     randX, randY = 6,1
        #     unvisited.remove((6,1))
        # else:
        randX,randY = unvisited.pop(random.randint(0, length-1))
        
        length -= 1
        randCount += 1
        #print("Checking " + str((randX,randY)))
        #Change this function to also update some list of bordering hidden squares
        markedMines, foundMines, length = recursiveMineCheck2(grid, dim, unvisited, length, borderHidden, KB, randX, randY, markedMines, foundMines)
    
    #pprint.pprint(KB)
    #print(len(borderHidden))
    numMines = markedMines + foundMines
    print("Score: " + str(float(markedMines)/numMines))
    print("Guesses: " + str(randCount))
    if(not checkKB(grid, KB)):
        print("Marked mines do not match actual mines")
    return markedMines, numMines, randCount

'''
[[ 0  0  1  1  1  0  0  0  0  0]
 [ 0  0  1 -1  1  0  1  1  1  0]
 [ 0  1  2  2  1  1  2 -1  1  0]
 [ 0  2 -1  2  0  1 -1  2  1  0]
 [ 0  2 -1  3  1  1  1  1  1  1]
 [ 0  1  2 -1  1  0  0  0  1 -1]
 [ 0  1  2  2  1  0  0  0  2  2]
 [ 0  1 -1  2  1  0  0  0  1 -1]
 [ 0  1  2 -1  1  0  0  0  1  1]
 [ 0  0  1  1  1  0  0  0  0  0]]
 '''


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
def guessAndCheck(grid, dim, borHid, KB):

    for (x,y) in borHid:
        for i in range(2):
            copyKB = copy.deepcopy(KB)
            if(i == 0):
                #Assume this square is a bomb
                copyKB[(x,y)][0] = -1
                guessBomb = extendAssumption(grid, copyKB, dim)
                if(guessBomb == False):
                    return 1, x, y
            else:
                #Assume this square is safe
                copyKB[(x,y)][0] = 2
                guessSafe = extendAssumption(grid, copyKB, dim)
                if(guessSafe == False):
                    return 2, x, y
    return 0,0,0

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
                return False

            if KB[(x,y)][4] == 0:
                continue

            neighbors = list(itertools.product(range(x-1, x+2), range(y-1, y+2)))
            properNeighbors = list(filter(lambda x: (0<=x[0]< dim and 0<=x[1]<dim), neighbors))
            properNeighbors.remove((x,y))
            
            #print((clue, revealedMines, x,y, KB[(x,y)]))
            
            if KB[(x,y)][1] - KB[(x,y)][3] == KB[(x,y)][4]:
                for i,j in properNeighbors:
                    if KB[(i,j)][0] == 0:
                        KB[(i,j)][0] = -1
                conclusion = True
            elif numNeighbors- KB[(x,y)][1]- KB[(x,y)][2] == KB[(x,y)][4]:
                #neighbors - clues - safeNeigh == hiddenNeigh
                #print("in safe bombs func")
                conclusion = True
                for i,j in properNeighbors:
                    if KB[(i,j)][0] == 0:
                        KB[(i,j)][0] = 2

    return True


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
            if y == 0 or y == dim -1:
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
        #displayGrid(grid, dim, KB)
        #input()
        KB[(x,y)][1] = clue
        KB[(x,y)][2], KB[(x,y)][3], KB[(x,y)][4] = countNeighborSquares(grid,KB, dim, x, y)
        addBorderHidden(borHid, KB, dim, x, y)
        #Add check for hidden == 0, conitnue
        #return markedMines, foundMines
        numNeighbors = 8
        if x == 0 or x== dim-1:
            numNeighbors -=3
        if y == 0 or y == dim -1:
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
        #print("Oop, ya blew up. Anyway")
        foundMines +=1
        KB[(x,y)][0] = -2
        #displayGrid(grid, dim, KB)
        #input()
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
b = 100

same = 0
improved = 0
worse = 0
falseP = 0
falseP2 = 0
# for i in range(1):
'''grid = [[ 0 , 0,  2, -1,  2,  1,  1,  2, -1, -1],
 [ 1,  1,  2, -1,  3,  2, -1,  3,  5, -1],
 [-1,  1,  2,  3, -1,  2,  2, -1,  3, -1],
 [ 1,  1,  1, -1,  2,  1,  2,  2,  3,  1],
 [ 0,  0,  1,  1,  2,  1,  2, -1,  1,  0],
 [ 0,  0,  0,  1,  3, -1,  3,  1,  1,  0],
 [ 0,  0,  0,  1, -1, -1,  3,  1,  1,  0],
 [ 1,  1,  0,  1,  2,  2,  2, -1,  1,  0],
 [-1,  2,  2,  1,  1,  0,  1,  1,  2,  1],
 [ 2, -1,  2, -1,  1,  0,  0,  0,  1, -1]]'''
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
def collectData(d, trials):
    density = []
    basic = []
    improv = []
    for j in range(1, 20):
        density.append(float(j)/20)
    for k in range(1, 20):
        b = int(d*d * float(k)/20)
        print(str(b))
        markedbasic = 0
        totNumbasic = 0
        markedImprov = 0
        totaNumImprov = 0
        for i in range(trials):
            grid = generateMineField(d, b)
            mark, num, guesses = basicAgent(grid, d, b)
            mark2, num2, guesses2 = improvedAgent(grid, d, b)
            markedbasic += mark
            totNumbasic += num
            markedImprov += mark2
            totaNumImprov += num2
        basicAverageScore = float(markedbasic)/totNumbasic
        improvAverageScore = float(markedImprov)/totaNumImprov
        basic.append(basicAverageScore)
        improv.append(improvAverageScore)
    with open("basic.txt", "w+") as f:
        for scores in basic:
            f.write(str(scores) + "\n")

    with open("improved.txt", "w+") as g:
        for scores in improv:
            g.write(str(scores) + "\n")

    plt.figure(1)
    plt.plot(density, basic, color = "m", linewidth = 4.0)
    plt.xlabel("Bomb Density")
    plt.ylabel("Average Final Score")
    plt.title("Basic Agent Average Final Score vs Bomb Density")
    plt.savefig("basic.png")
    plt.figure(2)
    plt.plot(density, improv, color = 'b', linewidth = 4.0)
    plt.xlabel("Bomb Density")
    plt.ylabel("Average Final Score")
    plt.title("Improved Agent Average Final Score vs Bomb Density")
    plt.savefig("improved.png")
    plt.figure(3)
    plt.plot(density, basic, color = "m", linewidth = 4.0, label = "Basic")
    plt.plot(density, improv, color = 'b', linewidth = 4.0, label = "Improved")
    plt.xlabel("Bomb Density")
    plt.ylabel("Average Final Score")
    plt.title("Average Scores for Strategies")
    plt.legend(loc = "upper right")
    plt.ylim(0, 1.0)
    plt.savefig("both.png")

#collectData(20, 25)


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
