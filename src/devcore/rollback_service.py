import subprocess
import os

class RollbackService:
    def __init__(self, project_dir="src/devcore/sandbox/project_build"):
        self.project_dir = project_dir
        self._init_repo()

    def _init_repo(self):
        if not os.path.exists(os.path.join(self.project_dir, ".git")):
            subprocess.run(["git", "init"], cwd=self.project_dir)
            subprocess.run(["git", "config", "user.email", "fsi@vitalis.dev"], cwd=self.project_dir)
            subprocess.run(["git", "config", "user.name", "FSI Agent"], cwd=self.project_dir)
            subprocess.run(["git", "add", "."], cwd=self.project_dir)
            subprocess.run(["git", "commit", "-m", "Initial State"], cwd=self.project_dir)

    def create_checkpoint(self, message):
        """Snapshots the current state."""
        subprocess.run(["git", "add", "."], cwd=self.project_dir)
        subprocess.run(["git", "commit", "-m", message], cwd=self.project_dir)

    def rollback(self):
        """Restores the previous stable state."""
        subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=self.project_dir)
        print("[+] ROLLBACK EXECUTED: State restored to previous commit.")
