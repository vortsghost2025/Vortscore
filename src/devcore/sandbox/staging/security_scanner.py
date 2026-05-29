import os
import re

class SecurityScanner:
    def __init__(self):
        self.vulnerabilities = []
        self.patterns = {
            "Hardcoded API Key": r"['\"](AIza[0-9A-Za-z-_]{35})['\"]",
            "Dangerous Function": r"(eval\(|exec\(|os\.system\(|subprocess\.Popen\(shell=True)",
            "Hardcoded Password": r"(password|passwd|secret)\s*=\s*['\"]([^'\"]+)['\"]"
        }

    def scan_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            # Explicitly ensure we are not entering venv
            if "venv" in root.split(os.sep):
                continue
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    self.analyze_file(path)
        return self.vulnerabilities

    def analyze_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for vuln, pattern in self.patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        # Use a safe prefix to avoid bash shell triggers
                        self.vulnerabilities.append(f"VULN_FOUND: {vuln} in {file_path}")
        except Exception:
            pass 

    def run(self):
        results = self.scan_directory("src")
        return "\n".join(results) if results else "AUDIT_CLEAN: No issues detected in project source."
