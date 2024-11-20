import math
import sys
import os

def read_dimacs_rules(dir_path, file_names):
    clauses = {}
    for name in file_names:
        file = open(dir_path + name, 'r')
        if "4x4" in name:
            size = 4
        elif "9x9" in name:
            size = 9
        elif "16x16" in name:
            size = 16
        else:
            return
        clauses[size] = file.readlines()
    return clauses

def puzzle_to_dimacs(puzzle, grid_size, dimacs_rules, num):
    puzzle_rules = []
    puzzle_rules.extend(dimacs_rules)

    # already filled cells
    for i in range(len(puzzle)):
        if puzzle[i] == ".":
            continue
        if grid_size == 16:
            if puzzle[i].isalpha():
                k = 10 + ord(puzzle[i]) - ord("A")
            else:
                k = int(puzzle[i])
        else:
            k = int(puzzle[i])
        x = i // grid_size + 1
        y = i % grid_size + 1
        if grid_size == 16:
            var = 17**2 * x + 17 * y + k
        else:
            var = 10**2 * x + 10 * y + k

        puzzle_rules.append(f"{var} 0\n")
    
    return puzzle_rules

def convert_sudokus_to_dimacs(sudoku_file_name, dimacs):
    file = open(sudoku_file_name,"r")
    lines = file.readlines()

    result = []

    for (num, line) in enumerate(lines):
        line = line.strip()
        grid_size = int(math.sqrt(len(line)))
        if grid_size * grid_size != len(line):
            print(f"Error in line {line}: Length is not a perfect square")
            continue
        if grid_size not in dimacs:
            print(f"Rules not found for grid size {grid_size}")
            continue

        result.append(puzzle_to_dimacs(line, grid_size, dimacs[grid_size], num))
    return result

if __name__ == "__main__":
    sudoku_file_name = sys.argv[1]
    if not os.path.isfile(sudoku_file_name):
        print(f"Error: The file '{sudoku_file_name}' does not exist.")
        sys.exit(1)

    rule_files = ["sudoku-rules-4x4.txt", "sudoku-rules-9x9.txt", "sudoku-rules-16x16.txt"]
    rules_dir = "data/"
    dimacs = read_dimacs_rules(rules_dir, rule_files)
    result = convert_sudokus_to_dimacs(sudoku_file_name, dimacs)

    for num, puzzle_rules in enumerate(result):
        with open(f"sudoku_nr_{num}", "w") as output_file:
            for rule in puzzle_rules:
                output_file.write(rule)