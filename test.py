#import pygame
import numpy as np
import itertools
import random
#import setup
import copy
import pprint
from sympy import * 


A = [[1, 1, 1, 0, 1], [1, 0, 1, 1, 2]]
M = Matrix(A)
b = [1,2,0,0]

A = [[1, 1, 1, 0, 0, 0, 0, 0 ,0, 1], [1, 0, 1, 1, 0, 0, 0, 0, 0, 2], [0, 1, 1, 1, 0, 0, 0, 0, 0, 3], [0, 0, 0, 1, 0, 0, 0, 0, 0, 1]]
M = Matrix(A)

Mref = M.rref()
print("{}".format(Mref))