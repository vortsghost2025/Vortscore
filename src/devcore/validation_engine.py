import ast
import os

class ValidationEngine:
    @staticmethod
    def validate(path):
        """
        Validates syntax. If path is a file, validates that file.
        If path is a directory, validates all .py files recursively.
        """
        if os.path.isfile(path):
            return ValidationEngine._check_file(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        if not ValidationEngine._check_file(os.path.join(root, file)):
                            return False
            return True
        return False

    @staticmethod
    def _check_file(file_path):
        try:
            with open(file_path, "r") as f:
                source = f.read()
            ast.parse(source)
            return True
        except Exception as e:
            print(f"[!] Syntax Error in {file_path}: {e}")
            return False
