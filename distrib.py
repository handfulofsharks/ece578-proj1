import numpy as np
import math

# function that generates the distribution of slots that 
# frames are placed in the transmission queue
#
# inputs:
# l = lambda
# t = simulation time
# t_slot = slot duration
#
# returns:
# x = list of slots for transmission
def generateDistribution(l, t, t_slot=10e-6):
    u = np.random.uniform(size=(l*t))
    x = [-(1/l) * math.log(1-i) for i in u]
    x = [math.ceil(i/t_slot) for i in x]
    x = list(np.cumsum(x))
    return x
