import os

class WorkspaceBuilder:
    def create_project(self, name, structure):
        os.makedirs(name, exist_ok=True)
        for folder in structure:
            os.makedirs(os.path.join(name, folder), exist_ok=True)
        return f"[+] Project '{name}' scaffolded."
