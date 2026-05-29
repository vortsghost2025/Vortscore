import json
import time
from pathlib import Path
from vitalis_ide.math_core.kernel import VitalisKernel
from vitalis_ide.ui.flow_manager import WaterFlowManager

class ThinkingProcess:
    def __init__(self):
        self.kernel = VitalisKernel()
        self.flow = WaterFlowManager()
        self.ledger = Path.home() / ".vitalis_workspace" / "truth_ledger.json"

    def run(self, input_vector, concept):
        self.flow.start_thinking()
        
        # Kernel execution
        processed = self.kernel.activation(self.kernel.matmul(input_vector, input_vector))
        
        # Log to Truth Ledger
        entry = {
            "timestamp": time.time(),
            "concept": concept,
            "status": "decoded",
            "kernel_signature": str(processed.sum())
        }
        with open(self.ledger, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
        self.flow.end_thinking("Logic pattern decoded and logged.")
        return processed
