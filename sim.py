import matplotlib.pyplot as plt
import numpy as np
import statistics
import random
import math

trials = 50000
n = 5
b = 0.25
C = 0.45

# 7 bag/laundry queue
q = list(range(n))

def preferred(x):
    # Savor 0
    return x != 0

def sim(i):
    print(f'\r{i}/{trials}', end='')
    # Take a load
    taken = list()
    for _ in range(random.randint(1, 2)):
        x = q.pop(0)
        taken.append(x)
        yield x
    # "Do laundry" - replace the taken load
    random.shuffle(taken)
    one = [x for x in taken if preferred(x)]
    two = [x for x in taken if not preferred(x)]
    q.extend(one)
    q.extend(two)

data = [ x for i in range(trials) for x in sim(i) ]
print()

data = [ data.count(i) / len(data) for i in range(n) ]
print(data)

avg = statistics.mean(data)
sd = statistics.stdev(data)
psd = statistics.pstdev(data)
var = statistics.variance(data)

print("Avg: ", avg)
print("SD:  ", sd)
print(avg - data[0])
print(b/n * C)
print()

# plt.hist(data, bins=n)
# plt.hist(list(range(len(data))), weights=data, bins=n)
# plt.plot(sorted(data))
# plt.scatter(data, range(len(data)))
# plt.show()

