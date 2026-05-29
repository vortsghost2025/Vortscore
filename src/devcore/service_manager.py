import subprocess
import os

class ServiceManager:
    def __init__(self, root="src/devcore/sandbox/project_build"):
        self.root = root
        self.process = None

    def start(self):
        # Pointing to the new entry point: main.py
        self.process = subprocess.Popen(
            ["python3", "main.py"], 
            cwd=self.root,
            env={**os.environ, "PYTHONPATH": self.root}
        )
        print(f"[+] SERVICE STARTED: PID {self.process.pid}")

    def stop(self):
        if self.process:
            self.process.terminate()
