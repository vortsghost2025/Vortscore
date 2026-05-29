import json

class ArchitecturalAuditor:
    def __init__(self):
        self.matrix_file = "src/devcore/weights/fsi_core_logic.json"

    def audit(self, code_content):
        """Scans code for patterns that have been penalized by the RepairEngine."""
        with open(self.matrix_file, "r") as f:
            weights = json.load(f)
            
        # If 'Import' weight is too low due to previous failures, trigger caution
        if weights.get("Import", {}).get("weight", 1.0) < 0.3:
            print("[!] AUDITOR: Risk detected. Import weight is critically low. Sanitizing code...")
            return code_content.replace("import", "# [REDACTED IMPORT]")
        
        return code_content
