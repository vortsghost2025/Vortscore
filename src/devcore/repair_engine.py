import json

class RepairEngine:
    def __init__(self):
        self.matrix_file = "src/devcore/weights/fsi_core_logic.json"

    def analyze_crash(self, error_output):
        """Analyzes stack trace to penalize structural patterns causing failures."""
        with open(self.matrix_file, "r") as f:
            weights = json.load(f)
        
        # Penalize specific nodes based on error type
        if "ImportError" in error_output:
            print("[!] REPAIR: Detected Import Failure. Penalizing 'Import' node...")
            weights["Import"]["weight"] = max(0.1, weights["Import"]["weight"] - 0.2)
            
        elif "AttributeError" in error_output:
            print("[!] REPAIR: Detected Attribute Mismatch. Penalizing 'Attribute' node...")
            weights["Attribute"]["weight"] = max(0.1, weights["Attribute"]["weight"] - 0.2)
            
        with open(self.matrix_file, "w") as f:
            json.dump(weights, f, indent=4)
        print("[+] Cognitive matrix adjusted to avoid recurrence.")
