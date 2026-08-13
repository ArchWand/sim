import sys
import random
import math
import itertools
import collections

# Given 4 cards, try to make 24 with them.

# Print solutions/unsolveable tuples
DEBUG = False
NDEBUG = False
UNARY = True

trials = 2000
n = 1 # Number of decks of cards

# Binary functions

def plus(a, b): return a + b
def minus(a, b): return a - b
def times(a, b): return a * b
def divide(a, b): return a / b if b != 0 and (a / b) > 1e-9 else False
# def exp(a, b): return a ** b if a > 1 and a < 100 and b < 30 else False
def exp(a, b): return a ** b if b == 2 or b == 3 else False
# def mod(a, b): return a % b if b != 0 and a >= b else False

ops = [plus, minus, times, divide, exp]
op_names = {
    plus: "+",
    minus: "-", 
    times: "*",
    divide: "/",
    exp: "^",
    # mod: "%",
}

# Unary functions

def sqrt(a):
    return math.sqrt(a) if a > 0 and a != 1 and a < sys.float_info.max else False
def fact(a): return math.factorial(int(round(a))) if a >= 0 and a != 1 and a != 4 and abs(a - round(a)) < 1e-9 and a <= 50 else False

unary_ops = [sqrt, fact]
# Format: operation: (name, is_prefix)
unary_op_names = {
    fact: ("!", False),
    sqrt: ("√", True),
}

def test_unary(result, expr):
    """
    Try each unary operation for particular result
    """
    yield (result, expr)
    if not UNARY: return
    for unary_op in unary_ops:
        result = unary_op(result)
        if result == False: continue
        op_name, is_prefix = unary_op_names[unary_op]
        expr = f"{op_name}({expr})" if is_prefix else f"({expr}){op_name}"
        yield (result, expr)

def generate_expr(values):
    """
    Recursively generate all possible parenthetizations.
    Returns tuples of (result, expression_string).
    """
    n = len(values)
    
    # Base case
    if n == 1:
        for result, expr in test_unary(values[0], str(values[0])):
            yield (result, expr)

    # Try all ways to split the values into left and right subtrees
    for i in range(1, n):
        left_vals = values[:i]
        right_vals = values[i:]
        
        # Recursively generate all left and right subtrees
        for left_result, left_expr in generate_expr(left_vals):
            for right_result, right_expr in generate_expr(right_vals):
                # Try all operators
                for op in ops:
                    result = op(left_result, right_result)
                    if result == False: continue
                    expr = f"({left_expr} {op_names[op]} {right_expr})"
                    for result, expr in test_unary(result, expr):
                        yield (result, expr)

def solve(tup, one_sol=True, debug=DEBUG, ndebug=NDEBUG):
    sols = []
    for perm in itertools.permutations(tup):
        for result, expr in generate_expr(list(perm)):
            if result == 24:
                if debug: print(expr)
                if one_sol: return True
                else: sols.append(expr)
    if ndebug: print(list(tup))
    return False if one_sol else sorted(sols, key=len, reverse=True)

def solver(a, b, c, d):
    """
    Nicer interface for interactive solving.
    """
    sols = solve((a, b, c, d), one_sol=False, debug=DEBUG, ndebug=NDEBUG)
    if not sols or not type(sols) is list:
        print("Unsolveable!")
    else:
        for expr in sols:
            print(expr)

def draw_hands():
    """
    Generator that simulates drawing 4-card hands from a deck.
    """
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

def simulate_hands():
    hands = draw_hands()
    count, total = 0, 0
    for i in range(trials):
        print(f'{i}/{trials}', end='\r')
        if solve(next(hands)): count += 1
        total += 1
    return count, total

def count_permutations():
    ABCD = 100000 * 4/52 * 4/51 * 4/50 * 4/49
    AABC = 100000 * 4/52 * 3/51 * 4/50 * 4/49 
    AABB = 100000 * 4/52 * 3/51 * 4/50 * 3/49
    AAAB = 100000 * 4/52 * 3/51 * 2/50 * 4/49
    AAAA = 100000 * 4/52 * 3/51 * 2/50 * 1/49

    count, total = 0, 0
    for i, tup in enumerate(itertools.combinations_with_replacement(list(range(1,14)), 4)):
        print(f'{i}/1820', end='\r')
        unique_counts = collections.Counter(tup)
        counts = sorted(unique_counts.values(), reverse=True)
        if counts == [4]:            p = AAAA
        elif counts == [3, 1]:       p = AAAB
        elif counts == [2, 2]:       p = AABB
        elif counts == [2, 1, 1]:    p = AABC
        else:                        p = ABCD

        if solve(tup): count += p
        total += p
    return count, total

if __name__ == "__main__":
    count, total = simulate_hands()
    # count, total = count_permutations()
    print(f"Solveable = {count/total}")
    print()
