import os

class SovereignKernel:
    def __init__(self, workspace_path):
        self.root = os.path.abspath(workspace_path)

    def write_code(self, file_path, code):
        full_path = os.path.join(self.root, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(code)
        print(f"[KERNEL] Written: {full_path}")
        return full_path

    def scaffold_module(self, module_name):
        module_dir = os.path.join(self.root, module_name)
        os.makedirs(module_dir, exist_ok=True)
        init_path = os.path.join(module_dir, "__init__.py")
        with open(init_path, 'w') as f:
            f.write(f"# {module_name} module\n")
        print(f"[KERNEL] Scaffolded: {module_dir}")
        return module_dir
