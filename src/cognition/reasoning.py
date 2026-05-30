"""
EmergentReasoningModes — Vitalis FSI

The system doesn't think the same way about every problem.
Context activates different reasoning modes.
Modes emerge from accumulated resonance — not hardcoded rules.

Four primary modes:
  EXPLORATORY  — novel territory, high creativity bias
  ANALYTICAL   — known domain, high precision bias
  RECOVERY     — failure context, high caution bias
  EXECUTION    — clear task, high speed bias
"""
import numpy as np
import os
import json
from vitalis_ide.math_core.kernel import VitalisKernel
from src.cognition.personality import PersonalityMatrix

MODE_SIGNATURES = {
    "EXPLORATORY": "new unknown explore discover create novel invent",
    "ANALYTICAL":  "analyze verify test validate check audit review",
    "RECOVERY":    "fail error broken fix repair debug recover heal",
    "EXECUTION":   "run execute deploy build scaffold write generate fast",
}

MODE_PARAMS = {
    "EXPLORATORY": {"similarity_threshold": 0.3, "creativity_boost": 1.5, "caution": 0.3},
    "ANALYTICAL":  {"similarity_threshold": 0.6, "creativity_boost": 0.7, "caution": 0.8},
    "RECOVERY":    {"similarity_threshold": 0.4, "creativity_boost": 0.5, "caution": 1.5},
    "EXECUTION":   {"similarity_threshold": 0.5, "creativity_boost": 1.0, "caution": 0.5},
}

class ReasoningEngine:
    def __init__(self):
        self.kernel = VitalisKernel()
        self.personality = PersonalityMatrix()
        self.mode_vectors = {
            mode: self.kernel.vectorize_tokens(sig.split(), positional=False)
            for mode, sig in MODE_SIGNATURES.items()
        }
        self.current_mode = "EXECUTION"
        self.mode_history = []

    def detect_mode(self, context: str) -> str:
        """
        Given a context string, find the closest reasoning mode.
        This is emergence — the mode isn't chosen, it crystallizes
        from the similarity between context and mode signatures.
        """
        ctx_vec = self.kernel.vectorize_tokens(context.lower().split(), positional=False)
        best_mode = "EXECUTION"
        best_sim = -1.0

        for mode, mode_vec in self.mode_vectors.items():
            sim = self.kernel.similarity(ctx_vec, mode_vec)
            if sim > best_sim:
                best_sim = sim
                best_mode = mode

        # Personality modulation — caution trait biases toward RECOVERY mode
        p = self.personality.traits
        if p["CAUTION"] > 0.7 and best_mode == "EXECUTION":
            best_mode = "ANALYTICAL"
        elif p["CREATIVITY"] > 0.7 and best_mode == "ANALYTICAL":
            best_mode = "EXPLORATORY"

        if best_mode != self.current_mode:
            print(f"[REASONING] Mode shift: {self.current_mode} → {best_mode} (sim={best_sim:.3f})")
        self.current_mode = best_mode
        self.mode_history.append(best_mode)
        return best_mode

    def get_params(self, mode: str = None) -> dict:
        return MODE_PARAMS.get(mode or self.current_mode, MODE_PARAMS["EXECUTION"])

    def report(self) -> dict:
        from collections import Counter
        history_counts = Counter(self.mode_history)
        return {
            "current_mode": self.current_mode,
            "mode_distribution": dict(history_counts),
            "personality_influence": self.personality.dominant_trait(),
            "params": self.get_params()
        }
