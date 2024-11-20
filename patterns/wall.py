import random
import numpy as np

def wall_pattern(sudoku, num_walls=None):
    grid_size = sudoku.shape[0]
    box_size = int(grid_size ** 0.5)
    num_boxes = grid_size

    #adjust nb of walls
    if num_walls is None:
        num_walls = max(1, num_boxes // 3)

    wall_pattern_sudoku = np.zeros((grid_size, grid_size), dtype=int)

    #random selection of boxes to apply the wall patterns to
    selected_boxes = random.sample(range(num_boxes), num_walls)
    for box in selected_boxes:
        start_row = (box // box_size) * box_size
        start_col = (box % box_size) * box_size

        #choice row n column
        if random.choice(['row', 'col']) == 'col':
            col_offset = random.randint(0, box_size - 1)
            for i in range(box_size):
                wall_pattern_sudoku[start_row + i, start_col + col_offset] = sudoku[start_row + i, start_col + col_offset]
        else:
            row_offset = random.randint(0, box_size - 1)
            for i in range(box_size):
                wall_pattern_sudoku[start_row + row_offset, start_col + i] = sudoku[start_row + row_offset, start_col + i]

    empty_cells = [(r, c) for r in range(grid_size) for c in range(grid_size) if wall_pattern_sudoku[r, c] == 0]
    extra_clues = random.sample(empty_cells, min(len(empty_cells), grid_size))  #proportional to the size
    for r, c in extra_clues:
        wall_pattern_sudoku[r, c] = sudoku[r, c]

    return wall_pattern_sudoku

def wall_pattern_dataset(sudokus, num_walls=None):
    wall_pattern_sudokus = []
    for sudoku in sudokus:
        wall_pattern_sudoku = wall_pattern(sudoku, num_walls)
        wall_pattern_sudokus.append(wall_pattern_sudoku)

    return wall_pattern_sudokus
