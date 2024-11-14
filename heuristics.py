import random
from collections import defaultdict

def get_literal_counts(clauses, literals):
    counts = defaultdict(lambda: [0, 0])
    for clause in clauses:
        for literal in literals:
            if literal > 0:
                counts[literal][0] += 1
            else:
                counts[literal][1] += 1
    return counts

def basic(literals):
    return literals[0]

def rand(literals):
    return random.choice(literals)

def dlcs(clauses, literals):
    counts = get_literal_counts(clauses, literals)
    literal = max(counts, key=lambda k: sum(counts[k]))
    if counts[literal][0] > counts[literal][1]:
        return literal, True
    else:
        return literal, False

def dlis(clauses, literals):
    counts = get_literal_counts(clauses, literals)
    literal = max(counts, key=lambda k: max(counts[k]))
    if counts[literal][0] > counts[literal][1]:
        return literal, True
    else:
        return literal, False

def jeroslow_wang(literals):
    return None

def mom(literals):
    return None
