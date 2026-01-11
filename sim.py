import matplotlib.pyplot as plt
import numpy as np
import statistics
import random
import math
import itertools

# Given 4 cards, try to make 24 with them.

# Print solutions/unsolveable tuples
DEBUG = False
NDEBUG = False

trials = 2000
n = 50

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

def infix(f):
    return Infix(f)

@infix
def plus(a, b): return a + b
@infix
def minus(a, b): return a - b
@infix
def times(a, b): return a * b
@infix
def divide(a, b): return a / b if b != 0 else math.pi
@infix
def exp(a, b): return a ** b if a != 0 and b < 100 else math.pi

ops = [plus, minus, times, divide, exp]
op_names = {
    plus: "+",
    minus: "-", 
    times: "*",
    divide: "/",
    exp: "^",
}

def solve(tup):
	for a, b, c, d in itertools.permutations(tup):
		for e1, e2, e3 in itertools.product(ops, repeat=3):
			if (((a |e1| b) |e2| c) |e3| d) == 24:
				if DEBUG: print(f"(({a} {op_names[e1]} {b}) {op_names[e2]} {c}) {op_names[e3]} {d}")
				return True
			if ((a |e1| (b |e2| c)) |e3| d) == 24:
				if DEBUG: print(f"({a} {op_names[e1]} ({b} {op_names[e2]} {c})) {op_names[e3]} {d}")
				return True
			if ((a |e1| b) |e2| (c |e3| d)) == 24:
				if DEBUG: print(f"({a} {op_names[e1]} {b}) {op_names[e2]} ({c} {op_names[e3]} {d})")
				return True
			if (a |e1| ((b |e2| c) |e3| d)) == 24:
				if DEBUG: print(f"{a} {op_names[e1]} (({b} {op_names[e2]} {c}) {op_names[e3]} {d})")
				return True
			if (a |e1| (b |e2| (c |e3| d))) == 24:
				if DEBUG: print(f"{a} {op_names[e1]} ({b} {op_names[e2]} ({c} {op_names[e3]} {d}))")
				return True
	if NDEBUG: print(list(tup))
	return False

def sim(i):
    print(f'{i}/{trials}', end='\r')
    expr = tuple(random.randint(1, 13) for _ in range(4))
    return 1 if solve(expr) else 0

data = [ sim(i) for i in range(trials) ]
# print(data)

avg = statistics.mean(data)
sd = statistics.stdev(data)
psd = statistics.pstdev(data)
var = statistics.variance(data)

print("Avg: ", avg)
print("SD:  ", sd)
print()

