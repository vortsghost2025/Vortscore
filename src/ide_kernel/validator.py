import subprocess
import pathlib
from typing import Tuple

class KernelValidator:
    @staticmethod
    def run_tests(target_path: str) -> Tuple[bool, str]:
        test_dir = pathlib.Path(target_path) / "tests"
        if not test_dir.is_dir():
            return True, "No tests found."
        # Use 'python3 -m pytest' to ensure the interpreter can find the module
        result = subprocess.run(["python3", "-m", "pytest", str(test_dir), "-q"], capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
