# import random
# import os

# output_file = "generated_symmetric_sudokus.txt"

# def generate_rotational_symmetric_sudoku(grid_size):
#     puzzle = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
#     num_clues = grid_size * 3 

#     clues = []
#     while len(clues) < num_clues // 2:
#         i, j = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
#         if (i, j) not in clues and (grid_size-1-i, grid_size-1-j) not in clues:
#             clues.append((i, j))

#     for i, j in clues:
#         value = random.randint(1, grid_size)
#         puzzle[i][j] = value
#         puzzle[grid_size-1-i][grid_size-1-j] = value

#     return puzzle

# def save_puzzles_to_file(puzzles, file_path):
#     with open(file_path, "w") as file:
#         for puzzle in puzzles:
#             single_line = ''.join(str(cell) if cell != '.' else '.' for row in puzzle for cell in row)
#             file.write(single_line + "\n")
#     print(f"Puzzles have been saved to '{file_path}'.")

# def generate_and_save_sudokus(grid_size, count, output_file):
#     puzzles = []
#     for _ in range(count):
#         puzzle = generate_rotational_symmetric_sudoku(grid_size)
#         puzzles.append(puzzle)
#     save_puzzles_to_file(puzzles, output_file)
#     print(f"{count} Sudoku puzzles have been generated and saved to '{output_file}'.")

# grid_size = 9
# count = 50
# generate_and_save_sudokus(grid_size, count, output_file)


import random

output_file = "valid_symmetric_sudokus.txt"

# Helper: Check if placing a number is valid
def is_valid(grid, row, col, num):
    for i in range(9):
        # Check row and column
        if grid[row][i] == num or grid[i][col] == num:
            return False
        # Check 3x3 subgrid
        if grid[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False
    return True

# Helper: Solve the Sudoku using backtracking
def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

# Generate a full valid Sudoku grid
def generate_full_sudoku():
    grid = [[0] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(grid, i, j, num):
                        grid[i][j] = num
                        if solve_sudoku(grid):
                            break
                        grid[i][j] = 0
                else:
                    return generate_full_sudoku()  # Restart if stuck
    return grid

# Remove numbers to create a puzzle while maintaining uniqueness
def create_puzzle_from_solution(grid, clues=30):
    puzzle = [row[:] for row in grid]
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)

    while len(cells) > 81 - clues:
        row, col = cells.pop()
        temp = puzzle[row][col]
        puzzle[row][col] = 0

        # # Check uniqueness
        # test_grid = [row[:] for row in puzzle]
        # if not has_unique_solution(test_grid):
        #     puzzle[row][col] = temp  # Restore if not unique

    return puzzle

# Check if a puzzle has a unique solution
def has_unique_solution(grid):
    solutions = []

    def backtrack(grid):
        if len(solutions) > 1:
            return  # More than one solution found
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num
                            backtrack(grid)
                            grid[row][col] = 0
                    return
        solutions.append([row[:] for row in grid])

    backtrack(grid)
    return len(solutions) == 1

# Save puzzles to a file
def save_puzzles_to_file(puzzles, file_path):
    with open(file_path, "w") as file:
        for puzzle in puzzles:
            single_line = ''.join(str(cell) if cell != 0 else '.' for row in puzzle for cell in row)
            file.write(single_line + "\n")
    print(f"Puzzles have been saved to '{file_path}'.")

# Main function to generate and save puzzles
def generate_and_save_valid_sudokus(count, output_file):
    puzzles = []
    for _ in range(count):
        full_solution = generate_full_sudoku()
        puzzle = create_puzzle_from_solution(full_solution, clues=30)
        puzzles.append(puzzle)
    save_puzzles_to_file(puzzles, output_file)

# Generate 50 valid Sudoku puzzles
generate_and_save_valid_sudokus(50, output_file)
