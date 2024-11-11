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
