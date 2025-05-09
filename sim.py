import matplotlib.pyplot as plt
import numpy as np
import statistics
import random
import math

trials = 50000
n = 50

def sim(i):
    print(f'{i}/{trials}', end='\r')
    return random.randint(0, 15)

data = [ sim(i) for i in range(trials) ]
# print(data)

avg = statistics.mean(data)
sd = statistics.stdev(data)
psd = statistics.pstdev(data)
var = statistics.variance(data)

print("Avg: ", avg)
print("SD:  ", sd)
# print("PSD: ", psd)
# print("Var: ", var)
print()

# plt.hist(data, bins=n, density=True)
# plt.hist(list(range(len(data))), weights=data, bins=n, density=True)
# plt.plot(sorted(data))
# plt.scatter(data, range(len(data)))
# plt.show()

