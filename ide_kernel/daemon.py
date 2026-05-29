import json, os, time, sys, logging
from .kernel import SovereignKernel
from .validator import KernelValidator
from .ledger import ProjectLedger
from .security import CDEPolicyEnforcer

# Append root to sys.path to allow imports from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.memory_bank import MemoryBank

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [DAEMON] - %(message)s')

class KernelDaemon:
    def __init__(self, workspace):
        self.root = os.path.abspath(workspace)
        self.task_file = os.path.join(self.root, "workspace_tasks.json")
        self.kernel = SovereignKernel(self.root)
        self.ledger = ProjectLedger(self.root)
        self.enforcer = CDEPolicyEnforcer(os.path.join(self.root, "cde_policy.yaml"))
        self.memory = MemoryBank(os.path.join(self.root, "vitalis_memory.json"))

    def start(self):
        logging.info("Vitalis Kernel Daemon active.")
        while True:
            if os.path.exists(self.task_file):
                try:
                    with open(self.task_file, 'r') as f:
                        task = json.load(f)
                except Exception as e:
                    logging.error(f"Failed to read task file: {e}")
                    os.remove(self.task_file)
                    continue
                
                intent = task.get('intent', 'unknown')
                
                # INTEGRITY GATE: The Security Gate
                if not self.enforcer.check_task(task):
                    logging.warning(f"Task blocked by Security Gate: {intent}")
                    self.memory.record_event("SECURITY_BLOCK", task)
                    os.remove(self.task_file)
                    continue
                
                # LOGGING: Record intent initiation
                self.memory.record_event("TASK_START", task)
                
                # EXECUTION: Scaffold or Write
                if intent == 'scaffold':
                    res = self.kernel.scaffold_module(task.get('module_name'))
                else:
                    res = self.kernel.write_code(task.get('file'), task.get('code'))
                
                # VALIDATION: Execute pytests
                target = self.root if intent == 'scaffold' else os.path.dirname(os.path.join(self.root, task.get('file', '')))
                success, output = KernelValidator.run_tests(target, sys.executable)
                
                # LEDGER & MEMORY COMMIT
                if success:
                    self.ledger.update_state(intent, "Completed")
                    self.memory.record_event("TASK_SUCCESS", {"intent": intent})
                    logging.info(f"Task {intent} succeeded.")
                else:
                    self.ledger.update_state(intent, "Failed")
                    self.memory.record_event("TASK_FAILED", {"intent": intent, "error": output})
                    logging.error(f"Task {intent} failed.")
                
                os.remove(self.task_file)
            time.sleep(0.5)

if __name__ == "__main__":
    KernelDaemon(os.getcwd()).start()
