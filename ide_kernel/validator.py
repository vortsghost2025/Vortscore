import subprocess, pathlib
from typing import Tuple

class KernelValidator:
    @staticmethod
    def run_tests(target_path: str, python_path: str = "python3") -> Tuple[bool, str]:
        test_dir = pathlib.Path(target_path) / "tests"
        if not test_dir.is_dir(): return True, "No tests."
        result = subprocess.run([python_path, "-m", "pytest", str(test_dir), "-q"], capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
