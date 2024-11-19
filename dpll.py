from heuristics import basic, jeroslow_wang, mom

k = 1

def is_clause_satisfied(clause, assignment):
    for literal in clause:
        if abs(literal) not in assignment:
            continue
        if assignment[abs(literal)] == (literal > 0):
            return True
    return False

def is_clause_unsatisfied(clause, assignment):
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
            if abs(literal) not in assignment or assignment[abs(literal)] != (literal > 0):
                shortened_clause.append(literal)

        if shortened_clause:
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
        literal_var, val = mom(clauses, literals, k)

    result = dpll(clauses, {**assignment, literal_var: val}, strategy, metrics)
    if result[0]:
        return result
    return dpll(clauses, {**assignment, literal_var: not val}, strategy, metrics)
