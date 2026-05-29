import os
class VitalisGenerator:
    def __init__(self, staging_dir):
        self.staging_dir = staging_dir
    def write_to_staging(self, module_name: str, code_string: str) -> str:
        os.makedirs(self.staging_dir, exist_ok=True)
        module_path = os.path.join(self.staging_dir, f"{module_name}.py")
        with open(module_path, "w", encoding="utf-8") as f:
            f.write(code_string)
        return module_path
