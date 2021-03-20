from basicAgent import *
from improvAgent import *
from betterImprovAgent import *
import matplotlib.pyplot as plt

def collectData(d, trials):
    #Set-up data structures
    density = []
    basic = []
    improv = []
    basicGuesses = []
    improvGuesses = []
    for j in range(1, 20):
        density.append(float(j)/20)

    for k in range(1, 20):
        #Run trials for each density
        b = int(d*d * float(k)/20)
        print(str(b))
        markedbasic = 0
        totNumbasic = 0
        markedImprov = 0
        totaNumImprov = 0
        basicGuessesNum = 0
        improvGuessesNum = 0

        for i in range(trials):
            #Run trial and record data
            grid = generateMineField(d, b)
            mark, num, guesses = basicAgent(grid, d)
            mark2, num2, guesses2 = improvedAgent(grid, d)
            markedbasic += mark
            totNumbasic += num
            markedImprov += mark2
            totaNumImprov += num2
            basicGuessesNum+=guesses
            improvGuessesNum+=guesses2

        #Calculate Scores and store    
        basicAverageScore = float(markedbasic)/totNumbasic
        improvAverageScore = float(markedImprov)/totaNumImprov
        basic.append(basicAverageScore)
        improv.append(improvAverageScore)
        basicGuesses.append(basicGuessesNum)
        improvGuesses.append(improvGuessesNum)

    #Store our collected data into output files
    with open("basic.txt", "w+") as f:
        for scores in basic:
            f.write(str(scores) + "\n")

    with open("improved.txt", "w+") as g:
        for scores in improv:
            g.write(str(scores) + "\n")

    with open("basicGuesses.txt", "w+") as h:
        for guess in basicGuesses:
            h.write(str(guess) + "\n")
    with open("improvGuesses.txt", "w+") as e:
        for guess in improvGuesses:
            e.write(str(guess) + "\n")

    #Plot everything with proper axes
    #Save each graph to a file
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

def collectDataTwo(d, trials):
    #Set up data structures
    density = []
    improv = []
    better = []
    betterGuesses = []
    for j in range(1, 20):
        density.append(float(j)/20)
    #get improved data from previous run
    with open("improved.txt", "r") as f:
        improv = f.readlines()
    improv = [float(x.strip()) for x in improv]
    for k in range(1, 20):
        #Run trials for each density
        b = int(d*d * float(k)/20)
        print(str(b))
        markedBetter = 0
        totNumBetter = 0
        betterGuessesNum = 0

        for i in range(trials):
            #run trials and record data
            grid = generateMineField(d, b)
            mark, num, guesses = improvedAgentBetter(grid, d, b)
            markedBetter += mark
            totNumBetter += num
            betterGuessesNum += guesses
        
        #calculate scores and store
        betterAverageScore = float(markedBetter)/totNumBetter
        better.append(betterAverageScore)
        betterGuesses.append(betterGuessesNum)
    
    #store data into output files for future use
    with open("better.txt", "w+") as g:
        for scores in better:
            f.write(str(scores) + "\n")
    with open("betterGuesses.txt", "w+") as h:
        for guess in betterGuesses:
            h.write(str(guess) + "\n")
    
    #Plot everythign and save each graph to file
    plt.figure(1)
    plt.plot(density, better, color = "r", linewidth = 4.0)
    plt.xlabel("Bomb Density")
    plt.ylabel("Average Final Score")
    plt.title("Better Decisions Agent Average Final Score vs Bomb Density")
    plt.savefig("better.png")

    plt.figure(2)
    plt.plot(density, improv, color = 'b', linewidth = 4.0)
    plt.plot(density, better, color = 'r', linewidth = 4.0)
    plt.xlabel("Bomb Density")
    plt.ylabel("Average Final Score")
    plt.title("Average Scores for Better Decisions Agent and Improved Agents")
    plt.legend(loc = 'upper right')
    plt.ylim(0, 1.0)
    plt.savefig("betterimprov.png")

collectDataTwo(20, 25)    