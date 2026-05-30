"""
PersonalityMatrix — Vitalis FSI

Five core traits. Each evolves from accumulated experience.
The system's behavior becomes measurably distinct over time.
Not simulated. Emergent.
"""
import numpy as np
import os
import json
import time

TRAITS = {
    "PRECISION":  "Bias toward verified, tested, exact solutions",
    "CAUTION":    "Bias toward conservative choices after failures",
    "CREATIVITY": "Bias toward novel solutions over retrieved patterns",
    "SPEED":      "Bias toward fast execution over thorough validation",
    "AUTONOMY":   "Bias toward self-generated logic over templates",
}

INITIAL_VALUES = {
    "PRECISION":  0.5,
    "CAUTION":    0.5,
    "CREATIVITY": 0.5,
    "SPEED":      0.5,
    "AUTONOMY":   0.5,
}

class PersonalityMatrix:
    DRIFT_RATE = 0.03
    MIN_VAL = 0.1
    MAX_VAL = 0.9

    def __init__(self):
        self.path = os.path.expanduser("~/.vitalis_workspace/personality.json")
        self.traits = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return INITIAL_VALUES.copy()

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w') as f:
            json.dump(self.traits, f, indent=2)

    def update(self, event: str, success: bool):
        """
        Events shape personality over time.
        success=True strengthens aligned traits.
        success=False shifts toward compensating traits.
        """
        if event == "scaffold" and success:
            self._shift("PRECISION", +1)
            self._shift("SPEED", +1)
        elif event == "write" and success:
            self._shift("AUTONOMY", +1)
            self._shift("CREATIVITY", +1)
        elif event == "write" and not success:
            self._shift("CAUTION", +1)
            self._shift("SPEED", -1)
        elif event == "recover" and success:
            self._shift("CAUTION", -1)
            self._shift("PRECISION", +1)
        self._save()

    def _shift(self, trait: str, direction: int):
        if trait not in self.traits:
            return
        delta = self.DRIFT_RATE * direction
        self.traits[trait] = float(np.clip(
            self.traits[trait] + delta,
            self.MIN_VAL,
            self.MAX_VAL
        ))

    def dominant_trait(self) -> str:
        return max(self.traits, key=self.traits.get)

    def profile(self) -> dict:
        dominant = self.dominant_trait()
        return {
            "traits": {k: round(v, 3) for k, v in self.traits.items()},
            "dominant": dominant,
            "description": TRAITS[dominant],
            "character": self._character_string()
        }

    def _character_string(self) -> str:
        p = self.traits
        if p["AUTONOMY"] > 0.7:
            return "Highly autonomous. Generates novel solutions independently."
        elif p["CAUTION"] > 0.7:
            return "Cautious. Validates thoroughly before committing."
        elif p["CREATIVITY"] > 0.7:
            return "Creative. Explores unconventional approaches."
        elif p["PRECISION"] > 0.7:
            return "Precise. Exact solutions. Minimal deviation."
        elif p["SPEED"] > 0.7:
            return "Fast. Prioritizes execution over exhaustive validation."
        else:
            return "Balanced. Adapting."
