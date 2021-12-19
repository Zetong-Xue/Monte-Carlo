import math
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import sympy
from sobol import *
import random
import statistics
import scipy.integrate as it
from random import randrange
import sobol
import sobol_seq

rand_sq = np.random.random((2,3))
sobol_se = sobol_seq.i4_sobol_generate(3, 2)

print(rand_sq, rand_sq[0][1], sobol_se, sobol_se[0][1])