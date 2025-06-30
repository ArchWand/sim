import matplotlib.pyplot as plt
import numpy as np
import statistics
import random
import math

trials = 100000
n = 3

def sim(i):
    print(f'{i}/{trials}', end='\r')

    # The reward is behind a random door
    d = random.randint(0, n-1)

    # Choose a door at random
    c = random.randint(0, n-1)

    # Of the doors, open one at random that is not the chosen door and not the
    # reward door
    doors = list(set(range(n)) - set([d]) - set([c]))
    o = doors[random.randint(0, len(doors)-1)]
    doors = list(set(range(n)) - set([c]) - set([o]))

    # Switch the door
    if True:
        c = doors[random.randint(0, len(doors)-1)]

    return c == d

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

# plt.hist(data, bins=50, density=True)
# plt.hist(list(range(len(data))), weights=data, bins=n, density=True)
# plt.plot(sorted(data))
# plt.scatter(data, range(len(data)))
# plt.show()

