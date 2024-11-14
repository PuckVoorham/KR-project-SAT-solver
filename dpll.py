from heuristics import basic, rand, dlcs, dlis 

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

def dpll(clauses, assignment, strategy):
    clauses = update_clauses(clauses, assignment)
    if not clauses:
        return assignment

    if any(is_clause_unsatisfied(clause, assignment) for clause in clauses):
        return False

    unit_literal = find_unit_literal(clauses, assignment)
    if unit_literal is not None:
        new_assignment = {**assignment, abs(unit_literal): (unit_literal > 0)}
        return dpll(clauses, new_assignment, strategy)

    pure_literal = find_pure_literal(clauses, assignment)
    if pure_literal is not None:
        new_assignment = {**assignment, abs(pure_literal): pure_literal > 0}
        return dpll(clauses, new_assignment, strategy)

    literals = []
    for clause in clauses:
        for literal in clause:
            if abs(literal) not in assignment:
                literals.append(abs(literal))

    if strategy == 1:
        literal_var = basic(literals)
    elif strategy == 2:
        literal_var = basic(literals)
    else:
        literal_var = basic(literals)

    result_true = dpll(clauses, {**assignment, literal_var: True}, strategy)
    if result_true:
        return result_true
    result_false = dpll(clauses, {**assignment, literal_var: False}, strategy)
    return result_false
