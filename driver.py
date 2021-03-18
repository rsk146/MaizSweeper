import basicAgent as ba
import improvAgent as ia
import dataCollector as dc

#This is the main function that we run
#Sample code that we used for testing is shown below as comments
#Running data collector is uncommented right now

d = 20
b = 100

same = 0
improved = 0
worse = 0
falseP = 0
falseP2 = 0


dc.collectData(10, 20)

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
# for i in range(20):
#     grid = ba.generateMineField(d, b)
#     mark, num, guesses = ba.basicAgent(grid, d)
#     mark2, num2, guesses2 = ia.improvedAgent(grid, d)
#     if(mark == mark2):
#         same += 1
#     elif( mark < mark2):
#         improved += 1
#     else:
#         worse += 1

#     if(num != b):
#         falseP += 1
#         print("Oops, missed mines or false positives in Basic")
#     if(num2 != b):
#         falseP2 += 1
#         print("Oops, missed mines or false positives in Basic")
#     print("\n")

# print("\n\n")
# print("Improved: " + str(improved))
# print("Same: " + str(same))
# print("Worse: " + str(worse))
# print("False Flags Basic: " + str(falseP))
# print("False Flags Improved: " + str(falseP2))

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

