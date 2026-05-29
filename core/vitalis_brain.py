import json, os
from core.diagnostics import run_diagnostics

class Resp:
    def __init__(self, status):
        self.status = status

class VitalisBrain:
    def process(self, text: str):
        text = text.lower()
        if "status" in text or "diagnostics" in text:
            run_diagnostics()
            return Resp("Diagnostics report displayed.")
        
        elif "scaffold" in text:
            parts = text.split()
            if len(parts) >= 2:
                module_name = parts[1]
                task = {"intent": "scaffold", "module_name": module_name}
                with open("workspace_tasks.json", "w") as f: json.dump(task, f)
                return Resp(f"Task queued: Scaffold {module_name}")
        
        return Resp("Command not recognized. Try 'status' or 'scaffold <name>'.")
