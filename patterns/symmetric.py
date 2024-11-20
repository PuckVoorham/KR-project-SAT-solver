import random

grid_size = 9
sub_grid_size = 3

upper_half = []
diag = []
for i in range(grid_size):
    for j in range(grid_size):
        if i + j < grid_size - 1:
            upper_half.append((i,j))
        elif i + j == grid_size - 1:
            diag.append((i, j))

def generate_sudoku_with_symmetric_clues(sudoku):
    num_diag = random.choice([i for i in range(1,6)])
    num_clues = random.choice([i for i in range(27, 40)]) - num_diag
    num_clues -= num_clues % 2
    generated_game = ["." for _ in range(grid_size * grid_size)]
    diag_pts = random.sample(diag, k = num_diag)
    for point in diag_pts:
        var = 9 * point[0] + point[1]
        generated_game[var] = sudoku[var]
    symmetric_pts = random.sample(upper_half, k = (num_clues // 2))
    for point in symmetric_pts:
        var = 9 * point[0] + point[1]
        var_symmetric = 9 * (grid_size - 1 - point[1]) + (grid_size - 1 - point[0])
        generated_game[var] = sudoku[var]
        generated_game[var_symmetric] = sudoku[var_symmetric]
    return generated_game

