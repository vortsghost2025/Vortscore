import numpy as np
from src.hippocampus import Hippocampus
import hdc_engine

class Router:
    def __init__(self):
        self.brain = Hippocampus()
        self.next_slot = 0
        
    def process(self, raw_input):
        # 1. Map input to a vector
        # (Simplified encoding: using the sum of character codes as a seed)
        seed = sum(ord(c) for c in raw_input)
        np.random.seed(seed)
        vector = np.random.choice([-1, 1], size=10000).astype(np.int8)
        
        # 2. Routing logic
        # For this prototype, we store everything as 'new learning'
        self.brain.store(self.next_slot, vector)
        print(f"Router: Imprinted '{raw_input}' into slot {self.next_slot}")
        self.next_slot += 1
        return vector
