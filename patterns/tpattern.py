import random

grid_size = 9
sub_grid_size = 3

def var_in_boxes(boxes, var):
    x = var // grid_size
    y = var % grid_size
    for box in boxes:
        row_min = (box // sub_grid_size) * sub_grid_size
        row_max = (box // sub_grid_size) * sub_grid_size + 2
        col_min = (box % sub_grid_size) * sub_grid_size
        col_max = (box % sub_grid_size) * sub_grid_size + 2
        if x >= row_min and x <= row_max and y >= col_min and y <= col_max:
            return True
    return False

def generate_sudoku_with_tpattern(sudoku, num_ts, num_clues):
    generated_game = ["." for _ in range(grid_size * grid_size)]
    boxes = random.sample([i for i in range(grid_size)], num_ts)
    for box in boxes:
        x = box // sub_grid_size
        y = box % sub_grid_size
        upward_t = random.choice([True, False])
        if upward_t:
            rows = [x*sub_grid_size + 1, x*sub_grid_size + 2]
            cols = [y*sub_grid_size, y*sub_grid_size + 2]            
        else:
            rows = [x*sub_grid_size, x*sub_grid_size + 1]
            cols = [y*sub_grid_size, y*sub_grid_size + 2]
        for row in rows:
            for col in cols:
                var = grid_size * row + col
                generated_game[var] = sudoku[var]
                num_clues -= 1

    vars = [i for i in range(grid_size * grid_size)]
    while num_clues > 0:
        var = random.choice(vars)
        if generated_game[var] != ".":
            continue
        if var_in_boxes(boxes, var):
            continue
        generated_game[var] = sudoku[var]
        num_clues -= 1    
    return generated_game

sudoku_file_name = "../1000 sudokus.txt"
input_file = open(sudoku_file_name, "r").readlines()
num_ts = [2,3,4]
num_clues = [i for i in range(25, 40)]
output_file = open("tpattern.txt", "w")
for line in input_file:
    line = line.strip()
    if grid_size * grid_size != len(line):
        continue
    game = generate_sudoku_with_tpattern(line, random.choice(num_ts), random.choice(num_clues))
    output_file.write("".join(game) + "\n")