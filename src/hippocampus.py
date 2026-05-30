import numpy as np
import os

class Hippocampus:
    def __init__(self, path=None):
        self.path = path or os.path.expanduser("~/.vitalis_workspace/hippocampus.npy")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if os.path.exists(self.path):
            self.memory = np.load(self.path, allow_pickle=True).item()
        else:
            self.memory = {}

    def store(self, slot, vector):
        self.memory[slot] = vector
        np.save(self.path, self.memory)

    def recall(self, slot):
        return self.memory.get(slot, None)

    def all_slots(self):
        return list(self.memory.keys())
