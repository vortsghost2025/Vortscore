"""
Resonance Engine.
Success strengthens weights. Failure weakens them.
The system learns from its own execution history.
No backpropagation. No gradient descent. Pure HDC resonance.
"""
import numpy as np
import os

class ResonanceEngine:
    LEARNING_RATE = 0.05
    MAX_WEIGHT = 2.0
    MIN_WEIGHT = 0.1

    def __init__(self):
        self.path = os.path.expanduser("~/.vitalis_workspace/resonance_weights.npy")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.weights = np.load(self.path, allow_pickle=True).item() \
            if os.path.exists(self.path) else {}

    def _save(self):
        np.save(self.path, self.weights)

    def reinforce(self, pattern_key: str, success: bool):
        w = self.weights.get(pattern_key, 1.0)
        if success:
            w = min(w * (1 + self.LEARNING_RATE), self.MAX_WEIGHT)
            print(f"[RESONANCE] Strengthened: {pattern_key} → {w:.3f}")
        else:
            w = max(w * (1 - self.LEARNING_RATE), self.MIN_WEIGHT)
            print(f"[RESONANCE] Weakened:     {pattern_key} → {w:.3f}")
        self.weights[pattern_key] = w
        self._save()

    def get_weight(self, pattern_key: str) -> float:
        return self.weights.get(pattern_key, 1.0)

    def top_patterns(self, n=10) -> list:
        sorted_w = sorted(self.weights.items(), key=lambda x: x[1], reverse=True)
        return sorted_w[:n]

    def report(self) -> dict:
        if not self.weights:
            return {"status": "No patterns learned yet"}
        return {
            "total_patterns": len(self.weights),
            "strongest": self.top_patterns(5),
            "avg_weight": round(float(np.mean(list(self.weights.values()))), 3)
        }
