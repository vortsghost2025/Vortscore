import json
import time
from pathlib import Path

class GhostExplain:
    def __init__(self):
        self.ledger = Path.home() / ".vitalis_workspace" / "truth_ledger.json"

    def get_narrative(self, answer_id=-1):
        if not self.ledger.exists(): return "No ledger found."
        with open(self.ledger, "r") as f:
            entries = [json.loads(line) for line in f]
        
        target = entries[answer_id]
        return (f"## 🧠 Ghost-Explain\n"
                f"**Concept:** {target.get('concept', 'Unknown')}\n"
                f"**Logic Path:** Analyzed {len(entries)} historical ledger events.\n"
                f"**Confidence Bias:** Based on {target.get('confidence', 'N/A')} signature.\n"
                f"**Verdict:** The model utilized the Truth Anchor established at {target.get('timestamp', 'N/A')}.")
