import os
import subprocess

# Path to the folder where CNF files are saved
puzzles_folder = "puzzles"

# Function to solve each CNF file using the SAT solver
def solve_sudoku_cnf(cnf_file_path):
    try:

        result = subprocess.run(["python3", 'SAT.py', cnf_file_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"SAT Solver for {cnf_file_path} was successful.")
            print(f"Solver Output:\n{result.stdout}")
        else:
            print(f"SAT Solver for {cnf_file_path} failed.")
            print(f"Error Output:\n{result.stderr}")
    except Exception as e:
        print(f"Error while solving {cnf_file_path}: {e}")

def solve_all_puzzles_in_folder():
    for filename in os.listdir(puzzles_folder):
        file_path = os.path.join(puzzles_folder, filename)
        print(f"Solving puzzle: {filename}")
        solve_sudoku_cnf(file_path)

# Run the solver for all CNF files
solve_all_puzzles_in_folder()
