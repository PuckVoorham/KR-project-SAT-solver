import os
from SAT import process_dimacs_sudoku
from sudoku_to_dimacs import convert_sudokus_to_dimacs, read_dimacs_rules

input_dir = "input_puzzles/"
heurestic_test_files = ["4x4.txt", "9x9.txt", "16x16.txt"]
rule_files = ["sudoku-rules-4x4.txt", "sudoku-rules-9x9.txt", "sudoku-rules-16x16.txt"]
rules_dir = "data/"
dimacs = read_dimacs_rules(rules_dir, rule_files)
output_dir = "result/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Heurestics testing
for file in heurestic_test_files:
    dimacs_sudokus = convert_sudokus_to_dimacs(input_dir + file, dimacs)
    solved_sudokus = []
    for i in range(1, 4):
        output_file = open(output_dir + "{}_heurestics_strategy{}.txt".format(file.split(".")[0], i), "w")
        for sudoku in dimacs_sudokus:
            solution, metrics, solving_time = process_dimacs_sudoku(sudoku, i)
            if solution is None:
                val = "UNSAT"
            else:
                val = "SAT"
            output_file.write("{:>5} {:>5} {:>5} {:10.4f}\n".format(val, metrics['backtracks'], metrics['decisions'], solving_time))
            output_file.flush()