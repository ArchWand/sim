import random
import math
import itertools

# Given 4 cards, try to make 24 with them.

# Print solutions/unsolveable tuples
DEBUG = False
NDEBUG = False

trials = 1820
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
def exp(a, b): return a ** b if a != 0 and a != 1 and b < 50 else math.pi
@infix
def mod(a, b): return a % b if b != 0 and a >= b else math.pi

ops = [plus, minus, times, divide, exp, mod]
op_names = {
    plus: "+",
    minus: "-", 
    times: "*",
    divide: "/",
    exp: "^",
    mod: "%",
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

ABCD = 100000 * 4/52 * 4/51 * 4/50 * 4/49
AABC = 100000 * 4/52 * 3/51 * 4/50 * 4/49 
AABB = 100000 * 4/52 * 3/51 * 4/50 * 3/49
AAAB = 100000 * 4/52 * 3/51 * 2/50 * 4/49
AAAA = 100000 * 4/52 * 3/51 * 2/50 * 1/49

count, total = 0, 0
for i, tup in enumerate(itertools.combinations_with_replacement(list(range(1,14)), 4)):
    print(f'{i}/{trials}', end='\r')
    unique_counts = collections.Counter(tup)
    counts = sorted(unique_counts.values(), reverse=True)
    if counts == [4]:            p = AAAA
    elif counts == [3, 1]:       p = AAAB
    elif counts == [2, 2]:       p = AABB
    elif counts == [2, 1, 1]:    p = AABC
    else:                        p = ABCD

    if solve(tup): count += p
    total += p

print(f"Solveable = {count/total}")
print()

