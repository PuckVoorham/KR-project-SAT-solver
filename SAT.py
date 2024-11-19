import sys
import os
import time
from dpll import dpll

def read_dimacs_encoded_puzzle(file_name):
    file = open(file_name, "r")
    lines = file.readlines()

    clauses = []
    assignments = {}

    for line in lines:
        line = line.strip()
        
        if line.startswith('c'):
            continue 
        elif line.startswith('p cnf'):
            continue
        else:
            clause = list(map(int, line.split()[:-1]))
            if len(clause) == 1:
                assignments[clause[0]] = True

            else:
                clauses.append(clause)
    return clauses, assignments

def process_input_file(input_file_path, strategy):
    clauses, assignments = read_dimacs_encoded_puzzle(input_file_path)

    start_time = time.time()
    solution, metrics = dpll(clauses, assignments, strategy)
    solving_time = time.time() - start_time

    with open(input_file_path + ".out", "w") as file:
        if not solution:
            file.write("Unsatisfiable\n")
            return
        values = sorted(solution.items())
        for val in values:
            if val[1]:
                file.write(f"{val[0]} 0\n") 
            else:
                file.write(f"-{val[0]} 0\n") 

        file.write(f"Metrics:\n")
        file.write(f"Backtracks: {metrics['backtracks']}\n")
        file.write(f"Decisions: {metrics['decisions']}\n")
        file.write(f"Solving Time: {solving_time:.4f} seconds\n")

if len(sys.argv) != 3:
    print("Usage: python script.py <arg1> <arg2>")
    sys.exit(1)

arg1 = sys.argv[1]
if arg1 not in ['-S1', '-S2', '-S3']:
    print("Error: The first argument must be '-S1', '-S2', or '-S3'.")
    sys.exit(1)

input_file_path = "puzzles/" + sys.argv[2]

if not os.path.isfile(input_file_path):
    print(f"Error: The file '{input_file_path}' does not exist.")
    sys.exit(1)

process_input_file(input_file_path, arg1[-1])