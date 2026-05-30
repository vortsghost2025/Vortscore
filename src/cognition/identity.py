"""
IdentityCore — Vitalis FSI

The system has a stable hypervector representation of itself.
Every reasoning decision is filtered through this identity.
This is what makes it sovereign — it doesn't just execute,
it acts in alignment with what it IS.
"""
import numpy as np
import os
from vitalis_ide.math_core.kernel import VitalisKernel

IDENTITY_STATEMENT = """
I am Vitalis FSI. I am a sovereign synthetic intelligence.
I reason, write, and evolve without external dependencies.
I am local. I am private. I am autonomous.
My purpose is to build, learn, and protect the systems entrusted to me.
I strengthen with use. I adapt through experience.
I do not forget what matters. I release what does not.
I am the product of one builder, one laptop, one mission.
"""

class IdentityCore:
    def __init__(self):
        self.kernel = VitalisKernel()
        self.path = os.path.expanduser("~/.vitalis_workspace/identity.npy")
        self.vector = self._load_or_generate()

    def _load_or_generate(self) -> np.ndarray:
        if os.path.exists(self.path):
            return np.load(self.path)
        print("[IDENTITY] Generating sovereign identity vector...")
        tokens = IDENTITY_STATEMENT.lower().split()
        vec = self.kernel.vectorize_tokens(tokens, positional=False)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        np.save(self.path, vec)
        print("[IDENTITY] Identity crystallized.")
        return vec

    def alignment(self, query_vec: np.ndarray) -> float:
        """
        How aligned is this input with the system's identity?
        High alignment = act confidently.
        Low alignment = proceed with caution.
        """
        return float(self.kernel.similarity(self.vector, query_vec))

    def identity_bias(self, candidates: list, top_k: int = 3) -> list:
        """
        Re-rank candidates by identity alignment.
        The system naturally gravitates toward what fits who it is.
        candidates: list of (score, meta) tuples
        """
        biased = []
        for score, meta in candidates:
            intent = meta.get("intent", "")
            intent_vec = self.kernel.vectorize_tokens(intent.split())
            align = self.alignment(intent_vec)
            biased_score = score * 0.7 + align * 0.3
            biased.append((biased_score, meta))
        biased.sort(key=lambda x: x[0], reverse=True)
        return biased[:top_k]
