import json
import os

class ContextSerializer:
    def __init__(self, workspace_path):
        self.root = workspace_path
        self.ledger_path = os.path.join(workspace_path, "project_ledger.json")

    def generate_context(self):
        # 1. Summarize Ledger
        ledger_data = {}
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                ledger_data = json.load(f)
        
        # 2. Map File Structure
        structure = []
        for root, dirs, files in os.walk(self.root):
            if '.git' in root or '__pycache__' in root or 'ide_kernel' in root:
                continue
            structure.append(f"{root}: {files}")

        # 3. Compile
        context = "--- PROJECT STATE ---\n"
        context += f"History: {json.dumps(ledger_data, indent=2)}\n"
        context += f"Filesystem: {structure}\n"
        context += "---------------------\n"
        return context

if __name__ == "__main__":
    serializer = ContextSerializer(os.getcwd())
    print(serializer.generate_context())
