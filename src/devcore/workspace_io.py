import os
import subprocess
import json

class WorkspaceIO:
    def __init__(self, sandbox_dir="src/devcore/sandbox"):
        self.sandbox_dir = sandbox_dir
        os.makedirs(self.sandbox_dir, exist_ok=True)

    def write_code_artifact(self, filename, content):
        """Writes a generated code file directly into the isolated sandbox environment."""
        target_path = os.path.join(self.sandbox_dir, filename)
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[+] Artifact written successfully: {target_path}")
            return target_path
        except IOError as e:
            print(f"[-] File system write failure: {e}")
            return None

    def execute_sandbox_test(self, filename):
        """Runs the written script in a secure, local subprocess to check syntax and execution viability."""
        target_path = os.path.join(self.sandbox_dir, filename)
        if not os.path.exists(target_path):
            return {"status": "error", "message": "Target artifact does not exist."}

        print(f"[+] Initializing live execution test for: {filename}...")
        try:
            # Run the script via local python3 interpreter with strict timeouts
            result = subprocess.run(
                ['python3', target_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "output": result.stdout.strip()
                }
            else:
                # Capture full traceback data for the dynamic feedback loop
                return {
                    "status": "runtime_failure",
                    "error": result.stderr.strip()
                }
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Execution exceeded maximum safety window (5s)."}

if __name__ == "__main__":
    # Self-test the I/O filesystem integration
    io_engine = WorkspaceIO()
    print("[+] Running filesystem integration self-test...")
    
    # Generate a temporary script to test compilation loop
    test_script = "def verify():\n    return 'FSI DevCore System Check: Pass'\nprint(verify())"
    path = io_engine.write_code_artifact("test_run.py", test_script)
    
    if path:
        test_result = io_engine.execute_sandbox_test("test_run.py")
        print(f"[+] Feedback execution result: {json.dumps(test_result, indent=2)}")
