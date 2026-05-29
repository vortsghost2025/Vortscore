import json
import os
import time
from src.ide_kernel.kernel import SovereignKernel
from src.ide_kernel.validator import KernelValidator
from src.ide_kernel.ledger import ProjectLedger

class KernelDaemon:
    def __init__(self, workspace_path):
        self.root = os.path.abspath(workspace_path)
        self.task_file = os.path.join(self.root, "workspace_tasks.json")
        self.kernel = SovereignKernel(self.root)
        self.ledger = ProjectLedger(self.root)

    def handle_failure(self, task, output):
        failure_path = os.path.join(self.root, "failure_report.json")
        failure_data = {
            "intent": "auto_debug",
            "original_task": task,
            "error_log": output
        }
        with open(failure_path, 'w') as f:
            json.dump(failure_data, f)
        print(f"[!] FAILURE LOGGED. Auto-Debug agent initialized: {failure_path}")

    def start(self):
        print("[+] FSI Kernel Daemon Active (Self-Healing Enabled).")
        while True:
            if os.path.exists(self.task_file):
                with open(self.task_file, 'r') as f:
                    try:
                        task = json.load(f)
                    except json.JSONDecodeError:
                        print("[!] Error reading task file. Retrying...")
                        time.sleep(1)
                        continue
                
                # 1. Execute
                intent = task.get('intent')
                try:
                    if intent == 'scaffold':
                        res = self.kernel.scaffold_module(task.get('module_name'))
                    else:
                        res = self.kernel.write_code(task.get('file'), task.get('code'))

                    # 2. Validate
                    target = self.root if intent == 'scaffold' else os.path.dirname(os.path.join(self.root, task.get('file', '')))
                    success, output = KernelValidator.run_tests(target)
                    
                    # 3. Memory & Recovery
                    if success:
                        self.ledger.update_state(intent, "Completed")
                        print(f"[SUCCESS] Action: {intent}. State Logged.")
                    else:
                        self.handle_failure(task, output)
                        self.ledger.update_state(intent, f"Failed: {output[:50]}...")
                except Exception as e:
                    print(f"[CRITICAL ERROR] {e}")
                
                os.remove(self.task_file)
            time.sleep(1)

if __name__ == "__main__":
    KernelDaemon(os.getcwd()).start()
