#!/usr/bin/env python3
import os
import json
import time
from src.ide_kernel.kernel import SovereignKernel
from src.ide_kernel.validator import KernelValidator
from src.ide_kernel.ledger import ProjectLedger

class SelfHealingLoop:
    def __init__(self, workspace_path=None):
        self.root = os.path.abspath(workspace_path or os.getcwd())
        self.failure_file = os.path.join(self.root, "failure_report.json")
        self.kernel = SovereignKernel(self.root)
        self.ledger = ProjectLedger(self.root)

    def run(self):
        print("[LOOP] Self-healing active. Watching for failures...")
        while True:
            if os.path.exists(self.failure_file):
                with open(self.failure_file, 'r') as f:
                    report = json.load(f)

                task = report.get("original_task", {})
                intent = task.get("intent")
                print(f"[LOOP] Failure detected for: {intent}. Attempting recovery...")

                try:
                    if intent == "scaffold":
                        self.kernel.scaffold_module(task.get("module_name"))
                    else:
                        self.kernel.write_code(task.get("file"), task.get("code"))

                    success, output = KernelValidator.run_tests(self.root)
                    if success:
                        self.ledger.update_state(intent, "Recovered")
                        print(f"[LOOP] Recovery successful: {intent}")
                        os.remove(self.failure_file)
                    else:
                        print(f"[LOOP] Recovery failed. Manual review needed.\n{output}")
                except Exception as e:
                    print(f"[LOOP] Critical recovery error: {e}")

            time.sleep(3)
