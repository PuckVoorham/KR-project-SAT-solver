import sys
import os
import time
from dpll import dpll
sys. setrecursionlimit(10000)

def read_dimacs_encoded_puzzle(lines):
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

def process_dimacs_sudoku(lines, strategy):
    clauses, assignments = read_dimacs_encoded_puzzle(lines)

    start_time = time.time()
    solution, metrics = dpll(clauses, assignments, strategy)
    solving_time = time.time() - start_time
    if not solution:
        return None, metrics, solving_time

    return sorted(solution.items()), metrics, solving_time

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python SAT.py <arg1> <arg2>")
        sys.exit(1)

    arg1 = sys.argv[1]
    if arg1 not in ['-S1', '-S2', '-S3']:
        print("Error: The first argument must be '-S1', '-S2', or '-S3'.")
        sys.exit(1)

    input_file_path = sys.argv[2]

    if not os.path.isfile(input_file_path):
        print(f"Error: The file '{input_file_path}' does not exist.")
        sys.exit(1)
    
    file = open(input_file_path, "r")
    lines = file.readlines()

    solution, _, _ = process_dimacs_sudoku(lines, arg1[-1])
    with open(input_file_path + ".out", "w") as file:
        if not solution:
            file.write("Unsatisfiable\n")
        else:
            for val in solution:
                if val[1]:
                    file.write(f"{val[0]} 0\n") 
                else:
                    file.write(f"-{val[0]} 0\n")