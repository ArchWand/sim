import random
import math
import itertools

# Given 4 cards, try to make 24 with them.

# Print solutions/unsolveable tuples
DEBUG = False
NDEBUG = False

trials = 1000
n = 1 # Number of decks of cards

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

def draw_hands():
    """Generator that simulates drawing 4-card hands from a deck."""
    deck = list(range(1, 14)) * n
    random.shuffle(deck)
    index = 0
    
    while True:
        # Shuffle when deck is empty or insufficient cards remain
        if index + 4 > len(deck):
            random.shuffle(deck)
            index = 0
        
        # Draw 4 cards
        hand = deck[index:index + 4]
        index += 4
        
        yield tuple(hand)

hands = draw_hands()
count, total = 0, 0
for i in range(trials):
    print(f'{i}/{trials}', end='\r')
    if solve(next(hands)): count += 1
    total += 1

print(f"Solveable = {count/total}")
print()

