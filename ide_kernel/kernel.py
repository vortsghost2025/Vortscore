import os
class SovereignKernel:
    def __init__(self, root): self.root = os.path.abspath(root)
    def write_code(self, path, content):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w') as f: f.write(content)
        return f"File updated: {path}"
    def scaffold_module(self, name):
        files = {
            f"app/modules/{name}/__init__.py": "",
            f"app/modules/{name}/logic.py": f"def process(): return '{name} active'",
            f"tests/test_{name}.py": "def test_module(): assert True"
        }
        return [self.write_code(p, c) for p, c in files.items()]
