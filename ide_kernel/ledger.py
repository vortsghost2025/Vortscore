import json, os
class ProjectLedger:
    def __init__(self, workspace): self.ledger_path = os.path.join(workspace, "project_ledger.json")
    def update_state(self, action, status):
        data = {}
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f: data = json.load(f)
        data[action] = status
        with open(self.ledger_path, 'w') as f: json.dump(data, f, indent=2)
