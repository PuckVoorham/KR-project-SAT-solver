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
    for key, value in scores.items():
        abs_key = abs(key)
        combined_scores[abs_key] = combined_scores.get(abs_key, 0) + value
    best_variable = max(combined_scores, key=combined_scores.get)
    if scores[best_variable] >= scores[-best_variable]:
        return best_variable, True
    return best_variable, False

def mom(clauses, literals, k=1):
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

def is_clause_satisfied(clause, assignment):
    for literal in clause:
        if abs(literal) not in assignment:
            continue
        if assignment[abs(literal)] == (literal > 0):
            return True
    return False

def is_clause_unsatisfied(clause, assignment):
    if len(clause) == 0:
        return True
    for literal in clause:
        if abs(literal) not in assignment:
            return False
        if assignment[abs(literal)] == (literal > 0):
            return False
    return True

def find_unit_literal(clauses, assignment):
    for clause in clauses:
        unassigned_literals = [literal for literal in clause if abs(literal) not in assignment]
        if len(unassigned_literals) == 1:
            return unassigned_literals[0]
    return None

def find_pure_literal(clauses, assignment):
    literals = set()
    for clause in clauses:
        for literal in clause:
            if abs(literal) not in assignment:
                literals.add(literal)
    for literal in literals:
        if -literal not in literals:
            return literal
    return None

def update_clauses(clauses, assignment):
    new_clauses = []
    
    for clause in clauses:
        # Remove satisfied clauses
        if is_clause_satisfied(clause, assignment):
            continue

        #Remove tautologies
        literals = set(clause)
        if any(-literal in literals for literal in clause):
            continue

        shortened_clause = []
        for literal in clause:
            if abs(literal) not in assignment:
                shortened_clause.append(literal)

        new_clauses.append(shortened_clause)
    
    return new_clauses

def dpll(clauses, assignment, strategy, metrics=None):

    if metrics is None:
        metrics = {"backtracks": 0, "decisions": 0}

    clauses = update_clauses(clauses, assignment)
    if not clauses:
        return assignment, metrics

    if any(is_clause_unsatisfied(clause, assignment) for clause in clauses):
        metrics["backtracks"] += 1
        return False, metrics

    unit_literal = find_unit_literal(clauses, assignment)
    if unit_literal is not None:
        new_assignment = {**assignment, abs(unit_literal): (unit_literal > 0)}
        return dpll(clauses, new_assignment, strategy, metrics)

    pure_literal = find_pure_literal(clauses, assignment)
    if pure_literal is not None:
        new_assignment = {**assignment, abs(pure_literal): pure_literal > 0}
        return dpll(clauses, new_assignment, strategy, metrics)

    literals = []
    for clause in clauses:
        for literal in clause:
            if abs(literal) not in assignment:
                literals.append(abs(literal))

    metrics ["decisions"] += 1

    if strategy == 1:
        literal_var, val = basic(literals)
    elif strategy == 2:
        literal_var, val = jeroslow_wang(clauses, literals)
    else:
        literal_var, val = mom(clauses, literals)

    result = dpll(clauses, {**assignment, literal_var: val}, strategy, metrics)
    if result[0]:
        return result
    return dpll(clauses, {**assignment, literal_var: not val}, strategy, metrics)
