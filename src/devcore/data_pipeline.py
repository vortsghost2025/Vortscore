import os
import shutil
import subprocess
import json
from src.devcore.syntax_ingester import SyntaxIngester

class DeveloperDataPipeline:
    def __init__(self, target_dir="src/devcore/training_data"):
        self.target_dir = target_dir
        self.ingester = SyntaxIngester()
        os.makedirs(self.target_dir, exist_ok=True)

    def fetch_and_ingest(self, repo_url, project_name):
        """
        Surgically clones a repository, extracts the abstract syntax trees,
        and purges the raw files to conserve disk space.
        """
        print(f"\n[=================================================]")
        print(f"[+] Initializing target acquisition: {project_name}")
        print(f"[=================================================]")
        
        clone_path = os.path.join(self.target_dir, project_name)
        
        # Step 1: Securely clone the target repository
        print(f"[*] Cloning source data from {repo_url}...")
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, clone_path],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            print("[-] Target acquisition failed. Check network or URL.")
            return

        # Step 2: Run the Syntax Ingester over the codebase
        print("[*] Engaging Syntax Ingester to extract logic structures...")
        structural_profiles = self.ingester.process_directory(clone_path)
        
        # Step 3: Compile the Hebbian Training Data
        output_file = os.path.join(self.target_dir, f"{project_name}_ast_profile.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structural_profiles, f, indent=2)
            
        print(f"[+] Structural logic mapped successfully. Profile contains {len(structural_profiles)} modules.")
        print(f"[+] Hebbian training payload saved to: {output_file}")

        # Step 4: Tactical Cleanup (Finesse Storage Management)
        print("[*] Purging raw repository files to conserve system partition space...")
        shutil.rmtree(clone_path)
        print("[+] Operation complete. System storage secured.")

if __name__ == "__main__":
    pipeline = DeveloperDataPipeline()
    # For our first live target, we will ingest an ultra-clean, minimalist framework 
    # to teach the model highly efficient routing and logic constraints.
    target_repo = "https://github.com/pallets/flask.git"
    pipeline.fetch_and_ingest(target_repo, "flask_core_logic")
