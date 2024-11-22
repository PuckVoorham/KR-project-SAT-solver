import os
import random
import numpy as np
from SAT import process_dimacs_sudoku
from sudoku_to_dimacs import convert_sudokus_to_dimacs, read_dimacs_rules
from patterns.symmetric import generate_sudoku_with_symmetric_clues
from patterns.tpattern import generate_sudoku_with_tpattern
from patterns.wall import wall_pattern

grid_size = 9

def get_grid_pos(var, grid_size):
    if grid_size == 16:
        val = 17
    else:
        val = 10
    x = var // (val ** 2)
    var = var % (val ** 2)
    y = var // val
    var = var % val
    k = var
    return x,y,k

def convert_solved_sudoku_to_grid(solved_dimacs):
    if grid_size * grid_size * grid_size != len(solved_dimacs):
        print(f"Error: Length is not a perfect square")
        return None
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    for (var, truth) in solved_dimacs:
        if not truth:
            continue
        x,y,k = get_grid_pos(var, grid_size)
        if grid[x - 1][y - 1] != ".":
            print(f"Error: Double assignment")
            return None
        grid[x - 1][y - 1] = str(k)
    return grid

# Pattern hypothesis on 9x9 puzzles
input_file = "input_puzzles/hypothesis.txt"
rule_files = ["sudoku-rules-4x4.txt", "sudoku-rules-9x9.txt", "sudoku-rules-16x16.txt"]
rules_dir = "data/"
dimacs = read_dimacs_rules(rules_dir, rule_files)

dimacs_sudokus = convert_sudokus_to_dimacs(input_file, dimacs)
solved_sudokus = []
output_file = open("solved/hypothesis.txt", "w")
for sudoku in dimacs_sudokus:
    solution, metrics, solving_time = process_dimacs_sudoku(sudoku, 1)
    if solution is None:
        continue
    grid = convert_solved_sudoku_to_grid(solution)
    if grid is None:
        continue
    result = "".join(["".join(row) for row in grid])
    solved_sudokus.append(result)
    output_file.write(result + "\n")
    output_file.flush()
print("No of sudokus solved: {} out of {}".format(len(solved_sudokus), len(dimacs_sudokus)))

baseline_sudokus = []
for sudoku in solved_sudokus:
    game = ["." for _ in range(81)]
    clue_positions = random.sample(range(0, 81), random.choice(range(25,40)))
    for position in clue_positions:
        game[position] = sudoku[position]
    output_file.write("".join(game) + "\n")

symmetric_sudokus = []
output_file = open("generated/symmetric.txt", "w")
for sudoku in solved_sudokus:
    game = generate_sudoku_with_symmetric_clues(sudoku)
    output_file.write("".join(game) + "\n")

output_file = open("generated/tpattern.txt", "w")
for sudoku in solved_sudokus:
    game = generate_sudoku_with_tpattern(sudoku)
    output_file.write("".join(game) + "\n")

output_file = open("generated/wall.txt", "w")
for sudoku in solved_sudokus:
    sudoku_grid = np.zeros((grid_size, grid_size), dtype=int)
    for i,val in enumerate(sudoku):
        x = i // grid_size
        y = i % grid_size
        sudoku_grid[x][y] = val
    game = wall_pattern(sudoku_grid)
    game = game.flatten()
    output_file.write("".join(map(str,game)).replace("0", ".") + "\n")
