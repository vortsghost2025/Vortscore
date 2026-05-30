import json
import os
import numpy as np
from src.hippocampus import Hippocampus

class ProjectLedger:
    def __init__(self, workspace_path):
        self.ledger_path = os.path.join(workspace_path, "project_ledger.json")
        self.hippocampus = Hippocampus()
        self.slot_path = os.path.join(workspace_path, "memory_slot.json")

    def _next_slot(self):
        if os.path.exists(self.slot_path):
            with open(self.slot_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"slot": 0}
        slot = data["slot"]
        data["slot"] = slot + 1
        with open(self.slot_path, 'w') as f:
            json.dump(data, f)
        return slot

    def update_state(self, action, status):
        # 1. Write to JSON ledger as before
        data = {}
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                data = json.load(f)
        data[action] = status
        with open(self.ledger_path, 'w') as f:
            json.dump(data, f)

        # 2. If successful, imprint into Hippocampus
        if "Completed" in status or "Recovered" in status:
            try:
                seed = sum(ord(c) for c in action)
                np.random.seed(seed)
                vector = np.random.choice([-1, 1], size=10000).astype(np.int8)
                slot = self._next_slot()
                self.hippocampus.store(slot, vector)
                print(f"[LEDGER] Action '{action}' imprinted to memory slot {slot}.")
            except Exception as e:
                print(f"[LEDGER] Memory imprint failed: {e}")
