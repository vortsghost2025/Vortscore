import numpy as np
from pathlib import Path

class VitalisKernel:
    def __init__(self):
        self.weights_path = Path.home() / ".vitalis_workspace" / "kernel.weights.npy"
        self.bias = np.load(self.weights_path) if self.weights_path.exists() else np.array([0.0])

    def matmul(self, a, b):
        # Apply the resonant bias (our 'learned' state) to the raw math
        return np.dot(a, b) + self.bias
