import random
import os

output_file = "generated_symmetric_sudokus.txt"

def generate_rotational_symmetric_sudoku(grid_size):
    puzzle = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    num_clues = grid_size * 3 

    clues = []
    while len(clues) < num_clues // 2:
        i, j = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        if (i, j) not in clues and (grid_size-1-i, grid_size-1-j) not in clues:
            clues.append((i, j))

    for i, j in clues:
        value = random.randint(1, grid_size)
        puzzle[i][j] = value
        puzzle[grid_size-1-i][grid_size-1-j] = value

    return puzzle

def save_puzzles_to_file(puzzles, file_path):
    with open(file_path, "w") as file:
        for puzzle in puzzles:
            for row in puzzle:
                file.write(''.join(str(cell) if cell != '.' else '.' for cell in row) + "\n")
            file.write("\n") 

def generate_and_save_sudokus(grid_size, count, output_file):
    puzzles = []
    for _ in range(count):
        puzzle = generate_rotational_symmetric_sudoku(grid_size)
        puzzles.append(puzzle)
    save_puzzles_to_file(puzzles, output_file)
    print(f"{count} Sudoku puzzles have been generated and saved to '{output_file}'.")

grid_size = 9
count = 50
generate_and_save_sudokus(grid_size, count, output_file)
