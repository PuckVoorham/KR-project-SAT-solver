import math
import os

output_folder = "puzzles/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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
        clauses[size] = file.read()
    return clauses

def puzzle_to_dimacs(puzzle, grid_size, dimacs_rules, num):
    assignments = []

    # already filled cells
    for i in range(len(puzzle)):
        if puzzle[i] == ".":
            continue
        k = int(puzzle[i])
        x = i // grid_size + 1
        y = i % grid_size + 1
        if grid_size == 16:
            var = 17**2 * x + 17 * y + k
        else:
            var = 10**2 * x + 10 * y + k

        assignments.append(var)
    
    # enocde to DIMACS format
    with open(output_folder + f"sudoku_nr_{num}", "w") as output_file:
        output_file.write(dimacs_rules)

        for literal in assignments:
            output_file.write(f"{literal} 0\n")

def convert_sudokus_to_dimacs(sudoku_file_name, dir_path, file_names):
    dimacs = read_dimacs_rules(dir_path, file_names)
    file = open(sudoku_file_name,"r")
    lines = file.readlines()

    for (num, line) in enumerate(lines):
        line = line.strip()
        grid_size = int(math.sqrt(len(line)))
        if grid_size * grid_size != len(line):
            print(f"Error in line {line}: Length is not a perfect square")
            continue
        if grid_size not in dimacs:
            print(f"Rules not found for grid size {grid_size}")
            continue

        puzzle_to_dimacs(line, grid_size, dimacs[grid_size], num)

sudoku_file_name = "damnhard.sdk.txt"
rule_files = ["sudoku-rules-4x4.txt", "sudoku-rules-9x9.txt", "sudoku-rules-16x16.txt"]
rules_dir = "data/"
convert_sudokus_to_dimacs(sudoku_file_name, rules_dir, rule_files)