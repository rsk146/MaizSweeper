from basicAgent import *
from improvAgent import *
import matplotlib.pyplot as plt

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
            mark, num, guesses = basicAgent(grid, d)
            mark2, num2, guesses2 = improvedAgent(grid, d)
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
