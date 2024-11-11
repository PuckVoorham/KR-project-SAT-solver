import os

repo_dir = os.path.dirname(__file__) 
data_dir = os.path.join(repo_dir, 'data')  

def read_and_update_DIMACS_encoded_rules(data_dir):

    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(data_dir, filename)
            clauses = []
            num_vars = 0
            
            if "4x4" in filename:
                num_vars = 64
            elif "9x9" in filename:
                num_vars = 729
            elif "16x16" in filename:
                num_vars = 4096

            else:
                print(f"Unknown grid size in filename: {filename}")
                continue
            
            # Read file and store clauses
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Parse each line and get clauses
            for line in lines:
                line = line.strip()
                
                if line.startswith('c'):
                    continue 
                elif line.startswith('p cnf'):
                    continue
                else:
                    clause = list(map(int, line.split()[:-1])) 
                    clauses.append(clause)
            
            num_clauses = len(clauses)

            # Write back the updated file
            with open(file_path, 'w') as file:
                
                file.write(f"p cnf {num_vars} {num_clauses}\n")
                
                # Rewrite the rest of the clauses
                for clause in clauses:
                    file.write(" ".join(map(str, clause)) + " 0\n")
            
            print(f"Updated {filename}: {num_vars} variables, {num_clauses} clauses")


read_and_update_DIMACS_encoded_rules(data_dir)



# def parse_sudoku_puzzles(filename):
#     """Reads Sudoku puzzles from a file, one per line."""
#     with open(filename, 'r') as file:
#         puzzles = [line.strip() for line in file.readlines()]
#     return puzzles

# def encode_cell(row, col, value):
#     """Encodes a cell's row, column, and value into a DIMACS variable."""
#     return 100 * row + 10 * col + value

# def encode_puzzle_to_dimacs(puzzle, clauses, output_file):
#     """Encodes a single Sudoku puzzle into DIMACS format and writes to output."""
#     dimacs_clauses = clauses

#     # Encode the puzzle's filled cells as clauses
#     for row in range(9):
#         for col in range(9):
#             value = puzzle[row * 9 + col]
#             if value.isdigit(): 
#                 literal = encode_cell(row + 1, col + 1, int(value))
#                 clauses.append(f"{literal} 0") 

#     # Write the DIMACS file
#     num_vars = 729  # 9x9x9 possible variables for Sudoku
#     num_clauses = len(dimacs_clauses)
#     with open(output_file, 'w') as file:
#         file.write(f"p cnf {num_vars} {num_clauses}\n")
#         for clause in dimacs_clauses:
#             file.write(f"{clause}\n")

# def convert_sudoku_puzzles_to_dimacs(puzzles_file, rules_file, output_dir):
#     """Converts all puzzles from a file to DIMACS format."""
#     puzzles = parse_sudoku_puzzles(puzzles_file)
#     for i, puzzle in enumerate(puzzles):
#         output_file = f"{output_dir}/sudoku_{i + 1}.cnf"
#         encode_puzzle_to_dimacs(puzzle, rules_file, output_file)
#         print(f"Converted puzzle {i + 1} to {output_file}")


# # convert_sudoku_puzzles_to_dimacs('1000 sudokus.txt', 'sudoku-rules-9x9.txt', 'output_dimacs')
