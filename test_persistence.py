from src.hippocampus import Hippocampus
import numpy as np

# 1. Initialize and store
brain = Hippocampus()
vec = np.random.choice([-1, 1], size=10000).astype(np.int8)
brain.store(0, vec)
brain.close()
del brain

# 2. Re-open and verify
brain_new = Hippocampus()
retrieved = brain_new.recall(0)

if np.array_equal(vec, retrieved):
    print("✅ Persistence confirmed: Memory survived the cycle.")
else:
    print("❌ Persistence failed.")
