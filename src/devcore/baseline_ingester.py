import os
import ast
import json

class BaselineIngester:
    def __init__(self):
        self.matrix_file = "src/devcore/weights/fsi_core_logic.json"
        
    def map_repository(self, target_dir):
        print(f"[*] VITALIS CORE: Initiating deep syntax extraction on {target_dir}...")
        
        baseline_weights = {}
        file_count = 0
        
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    filepath = os.path.join(root, file)
                    self._ingest_file(filepath, baseline_weights)
                    file_count += 1
                    
        self._commit_to_matrix(baseline_weights)
        print(f"[+] Baseline integration complete. Ingested {file_count} architectural files.")
        print(f"[+] Vitalis Core is no longer a blank slate.")

    def _ingest_file(self, filepath, weights_dict):
        try:
            with open(filepath, "r") as f:
                tree = ast.parse(f.read())
            
            # Extract nodes to build associative logic links
            for node in ast.walk(tree):
                node_type = type(node).__name__
                if node_type not in weights_dict:
                    weights_dict[node_type] = {"weight": 0.5, "associations": []}
                
                # Increment weight for frequently used structures
                weights_dict[node_type]["weight"] = round(weights_dict[node_type]["weight"] + 0.01, 4)
                
                # Map variable naming patterns and logic chains
                if isinstance(node, ast.FunctionDef):
                    if "function_design" not in weights_dict[node_type]["associations"]:
                        weights_dict[node_type]["associations"].append("function_design")
        except Exception as e:
            pass # Ignore unparseable files during bulk ingest

    def _commit_to_matrix(self, new_weights):
        if os.path.exists(self.matrix_file):
            with open(self.matrix_file, "r") as f:
                existing_weights = json.load(f)
        else:
            existing_weights = {}
            
        # Merge new baseline into existing matrix
        existing_weights.update(new_weights)
        
        with open(self.matrix_file, "w") as f:
            json.dump(existing_weights, f, indent=4)
