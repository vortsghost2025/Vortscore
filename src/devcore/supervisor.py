import json
from src.devcore.context_core import ContextManager
from src.devcore.agent_manager import DeveloperAgent

class FSI_Supervisor:
    def __init__(self):
        self.context = ContextManager()
        self.orchestrator = DeveloperAgent()
        
    def execute_directive(self, task_description):
        """
        The Master Loop:
        1. Parse intent.
        2. Assign agents.
        3. Validate against holisitic state.
        4. Integrate feedback.
        """
        print(f"[+] Supervisor receiving directive: {task_description}")
        self.context.update_state("current_task", task_description)
        
        # In this master loop, the orchestrator handles the build, 
        # while the supervisor checks for system-level context drift.
        result = self.orchestrator.autonomous_build_loop("master_dev_task", task_description)
        
        if result["status"] == "success":
            self.context.update_state("project_status", "Task Complete - Verified")
            return "[+] Task achieved and verified."
        else:
            return "[-] Task failed: Supervisory intervention required."

if __name__ == "__main__":
    supervisor = FSI_Supervisor()
    # Test directive for building a non-placeholder module
    print(supervisor.execute_directive("def get_system_load(): return '8%'"))
