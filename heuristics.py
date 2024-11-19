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
    return literals[0], True

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

def jeroslow_wang(clauses, literals):
    #two sided
    scores = {var: 0.0 for var in literals}
    scores.update({-var: 0.0 for var in literals})

    for clause in clauses:
        clause_weight = pow(2, -len(clause))
        for literal in clause:
            scores[literal] += clause_weight

    combined_scores = {}
    best_variable = max(combined_scores, key=combined_scores.get)
    if scores[best_variable] >= scores[-best_variable]:
        return best_variable, True
    return -best_variable, False

def mom(clauses, literals, k):
    min_clause_len = min(len(clause) for clause in clauses)
    smallest_clauses = [clause for clause in clauses if len(clause) == min_clause_len]
    counts = defaultdict(int)
    for clause in smallest_clauses:
        for literal in clause:
            counts[abs(literal)] += 1
    
    scores = defaultdict(float)
    for var in literals:
        scores[abs(var)] = counts[var] * (2 ** k) + counts[var]
    
    return max(scores, key=scores.get), True
