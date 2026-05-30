"""
MetaRulesEngine — Vitalis FSI

Rules are not hardcoded. They are HDC vectors.
Rules that correlate with success get reinforced.
Rules that correlate with failure get mutated or dropped.
New rules crystallize from repeated successful action sequences.

This is the system rewriting its own decision logic.
"""
import numpy as np
import os
import json
from vitalis_ide.math_core.kernel import VitalisKernel

class MetaRulesEngine:
    REINFORCEMENT_RATE = 0.1
    MUTATION_RATE = 0.05
    PRUNE_THRESHOLD = 0.2
    MAX_RULES = 50

    def __init__(self):
        self.kernel = VitalisKernel()
        self.path = os.path.expanduser("~/.vitalis_workspace/meta_rules.json")
        self.vec_path = os.path.expanduser("~/.vitalis_workspace/rule_vectors.npy")
        self._load()

    def _load(self):
        self.rules = {}
        self.rule_vectors = {}
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.rules = json.load(f)
        if os.path.exists(self.vec_path):
            self.rule_vectors = np.load(self.vec_path, allow_pickle=True).item()

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w') as f:
            json.dump(self.rules, f, indent=2)
        np.save(self.vec_path, self.rule_vectors)

    def crystallize(self, action_sequence: list, outcome: str):
        """
        Repeated successful action sequences crystallize into rules.
        The sequence becomes a rule the system applies automatically.
        """
        key = "→".join(action_sequence)
        vec = self.kernel.vectorize_tokens(action_sequence, positional=True)

        if key not in self.rules:
            self.rules[key] = {
                "sequence": action_sequence,
                "outcome": outcome,
                "confidence": 0.5,
                "uses": 0
            }
            self.rule_vectors[key] = vec
            print(f"[META-RULES] Rule crystallized: {key}")
        else:
            r = self.rules[key]
            if outcome == "success":
                r["confidence"] = min(r["confidence"] + self.REINFORCEMENT_RATE, 1.0)
            else:
                r["confidence"] = max(r["confidence"] - self.REINFORCEMENT_RATE, 0.0)
            r["uses"] += 1

        self._save()
        self._prune()

    def _prune(self):
        """Drop rules below confidence threshold."""
        to_drop = [k for k, v in self.rules.items()
                   if v["confidence"] < self.PRUNE_THRESHOLD and v["uses"] > 3]
        for k in to_drop:
            del self.rules[k]
            self.rule_vectors.pop(k, None)
            print(f"[META-RULES] Rule pruned: {k}")
        if to_drop:
            self._save()

    def match(self, context: str) -> dict:
        """Find the highest-confidence rule for this context."""
        ctx_vec = self.kernel.vectorize_tokens(context.split(), positional=False)
        best_match = None
        best_score = 0.0
        for key, vec in self.rule_vectors.items():
            sim = self.kernel.similarity(ctx_vec, vec)
            confidence = self.rules[key]["confidence"]
            score = sim * confidence
            if score > best_score:
                best_score = score
                best_match = self.rules[key]
        return {"rule": best_match, "score": round(best_score, 4)} if best_match else {}

    def report(self) -> dict:
        if not self.rules:
            return {"status": "No rules crystallized yet"}
        top = sorted(self.rules.items(), key=lambda x: x[1]["confidence"], reverse=True)[:5]
        return {
            "total_rules": len(self.rules),
            "top_rules": [{"sequence": v["sequence"],
                           "confidence": round(v["confidence"], 3),
                           "uses": v["uses"]} for _, v in top]
        }
