import json
import time

class ContextManager:
    def __init__(self):
        self.state = {
            "project_status": "initializing",
            "user_intent": "high_level_mastery",
            "active_anomalies": [],
            "last_thought_cycle": time.time()
        }
    
    def update_state(self, key, value):
        self.state[key] = value
        
    def get_holistic_view(self):
        """
        Synthesizes the project, technical debt, and user intent 
        into a single cognitive snapshot for the FMM.
        """
        return f"CONTEXT_SNAPSHOT: {json.dumps(self.state, indent=2)}"

if __name__ == "__main__":
    ctx = ContextManager()
    ctx.update_state("project_status", "Active: Building Core Orchestrator")
    print(ctx.get_holistic_view())
