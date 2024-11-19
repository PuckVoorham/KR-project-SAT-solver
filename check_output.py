import sys
import os
import math

def is_valid_sudoku(board, grid_size):
    def is_valid_block(block):
        return sorted(block) == list(range(1, grid_size + 1))
    
    for row in board:
        if not is_valid_block(row):
            return False
    
    # Check columns
    for col in range(grid_size):
        if not is_valid_block([board[row][col] for row in range(grid_size)]):
            return False
    
    sub_grid_size = int(math.sqrt(grid_size))
    # Check 3x3 sub-grids
    for i in range(0, grid_size, sub_grid_size):
        for j in range(0, grid_size, sub_grid_size):
            subgrid = [
                board[x][y]
                for x in range(i, i + sub_grid_size)
                for y in range(j, j + sub_grid_size)
            ]
            if not is_valid_block(subgrid):
                return False
    
    return True


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

def read_solved_sudoku(solved_dimacs):
    lines = solved_dimacs.readlines()
    grid_size = int(math.cbrt(len(lines)))
    if grid_size == 0:
        print("Unsat")
        return
    if grid_size * grid_size * grid_size != len(lines):
        print(f"Error: Length is not a perfect square")
        return
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    for line in lines:
        var = int(line.split(" ")[0])
        if var < 0:
            continue
        x,y,k = get_grid_pos(var, grid_size)
        if grid[x - 1][y - 1] != ".":
            print(f"Error: Double assignment")
            return
        grid[x - 1][y - 1] = k
    return grid

output_file_path = "puzzles/" + sys.argv[1]
if not os.path.isfile(output_file_path):
    print(f"Error: The file '{output_file_path}' does not exist.")
    sys.exit(1)
print_board = sys.argv[2]
solved_dimacs = open(output_file_path, 'r')
grid = read_solved_sudoku(solved_dimacs)
print(is_valid_sudoku(grid, len(grid)))

if print_board == "1":
    for row in grid:
        print(" ".join(map(str, row)))
