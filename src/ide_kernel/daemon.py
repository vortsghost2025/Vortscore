import json, os, time
from src.ide_kernel.kernel import SovereignKernel
from src.ide_kernel.validator import KernelValidator
from src.ide_kernel.ledger import ProjectLedger
from src.brain.resonance import ResonanceEngine

class KernelDaemon:
    def __init__(self, workspace_path):
        self.root = os.path.abspath(workspace_path)
        self.task_file = os.path.join(self.root, "workspace_tasks.json")
        self.kernel = SovereignKernel(self.root)
        self.ledger = ProjectLedger(self.root)
        self.resonance = ResonanceEngine()

    def handle_failure(self, task, output):
        path = os.path.join(self.root, "failure_report.json")
        with open(path, 'w') as f:
            json.dump({"intent":"auto_debug","original_task":task,"error_log":output}, f)
        self.resonance.reinforce(task.get('intent','unknown'), success=False)
        print(f"[!] FAILURE LOGGED. Auto-Debug initialized: {path}")

    def start(self):
        print("[+] FSI Kernel Daemon Active (Self-Healing + Resonance Enabled).")
        while True:
            if os.path.exists(self.task_file):
                with open(self.task_file, 'r') as f:
                    try: task = json.load(f)
                    except json.JSONDecodeError:
                        print("[!] Error reading task file. Retrying...")
                        time.sleep(1)
                        continue
                intent = task.get('intent')
                try:
                    if intent == 'scaffold':
                        res = self.kernel.scaffold_module(task.get('module_name'))
                    else:
                        res = self.kernel.write_code(task.get('file'), task.get('code'))
                    target = self.root if intent == 'scaffold' else os.path.dirname(
                        os.path.join(self.root, task.get('file', '')))
                    success, output = KernelValidator.run_tests(target)
                    if success:
                        self.ledger.update_state(intent, "Completed")
                        self.resonance.reinforce(intent, success=True)
                        try:
                            from src.brain.pattern_library import PatternLibrary
                            PatternLibrary().store(intent, task.get('code') or intent, task.get('file'))
                        except Exception as e:
                            print(f"[DAEMON] Pattern learning skipped: {e}")
                        print(f"[SUCCESS] Action: {intent}. Resonance reinforced.")
                    else:
                        self.handle_failure(task, output)
                        self.ledger.update_state(intent, f"Failed: {output[:50]}...")
                except Exception as e:
                    print(f"[CRITICAL ERROR] {e}")
                os.remove(self.task_file)
            time.sleep(1)

if __name__ == "__main__":
    KernelDaemon(os.getcwd()).start()
