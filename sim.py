import matplotlib.pyplot as plt
import numpy as np
import statistics
import random
import math

trials = 50000
n = 50

# 7 bag/laundry queue
q = list(range(n))

def sim(i):
    print(f'{i}/{trials}', end='\r')
    taken = list()
    for _ in range(random.randint(15, 25)):
        x = q.pop(0)
        taken.append(x)
        yield x
    random.shuffle(taken)
    bound = 15
    one = [x for x in taken if x < bound]
    two  = [x for x in taken if x >= bound]
    q.extend(one)
    q.extend(two)

data = [ x for i in range(trials) for x in sim(i) ]
data = [ data.count(i) for i in range(n) ]
print(q)
print(data)

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
plt.hist(list(range(len(data))), weights=data, bins=50, density=True)
# plt.plot(sorted(data))
# plt.scatter(data, range(len(data)))
plt.show()

