import numpy as np
import math

def generateDistribution(l, t):
    u = np.random.uniform(size=(l*t))
    x = [-(1/l) * math.log(1 -i ) for i in u]
    return x
