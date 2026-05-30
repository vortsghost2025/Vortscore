import numpy as np
import os
import sys
sys.path.insert(0, os.path.expanduser("~/vitalis_devcore"))
from vitalis_ide.math_core.kernel import VitalisKernel

class InferenceEngine:
    def __init__(self):
        self.kernel = VitalisKernel()

    def reason(self, prompt: str) -> str:
        tokens = prompt.strip().split()
        vec = self.kernel.vectorize_tokens(tokens)
        confidence = float(np.mean(np.abs(vec)))
        if "scaffold" in prompt.lower():
            return "scaffold"
        elif "write" in prompt.lower() or "fix" in prompt.lower():
            return "write"
        else:
            return f"[INFER] Confidence={confidence:.3f} | Input={prompt[:80]}"

    def embed(self, text: str) -> np.ndarray:
        return self.kernel.vectorize_tokens(text.strip().split())
