import numpy as np
import os
import json
import time

class Hippocampus:
    """
    Biologically-inspired vector memory.
    Memories strengthen with use. Memories decay without use.
    Based on Ebbinghaus forgetting curve.
    """

    def __init__(self, path=None):
        self.path = path or os.path.expanduser("~/.vitalis_workspace/hippocampus.npy")
        self.meta_path = os.path.expanduser("~/.vitalis_workspace/hippocampus_meta.json")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.memory = np.load(self.path, allow_pickle=True).item() if os.path.exists(self.path) else {}
        self._load_meta()

    def _load_meta(self):
        if os.path.exists(self.meta_path):
            with open(self.meta_path) as f:
                self.meta = json.load(f)
        else:
            self.meta = {}

    def _save_meta(self):
        with open(self.meta_path, 'w') as f:
            json.dump(self.meta, f, indent=2)

    def _strength(self, slot) -> float:
        """Ebbinghaus forgetting curve: R = e^(-t/S)"""
        if slot not in self.meta:
            return 1.0
        m = self.meta[slot]
        t = (time.time() - m.get("last_access", time.time())) / 3600
        S = m.get("stability", 24.0)
        return float(np.exp(-t / S))

    def store(self, slot, vector):
        slot = str(slot)
        self.memory[slot] = vector
        now = time.time()
        if slot not in self.meta:
            self.meta[slot] = {"created": now, "access_count": 0, "stability": 24.0}
        self.meta[slot]["last_access"] = now
        np.save(self.path, self.memory)
        self._save_meta()

    def recall(self, slot):
        slot = str(slot)
        vec = self.memory.get(slot)
        if vec is not None:
            # Strengthen on recall — spaced repetition
            if slot in self.meta:
                self.meta[slot]["access_count"] = self.meta[slot].get("access_count", 0) + 1
                self.meta[slot]["stability"] = min(
                    self.meta[slot].get("stability", 24.0) * 1.2, 720.0
                )
                self.meta[slot]["last_access"] = time.time()
                self._save_meta()
        return vec

    def forget_weak(self, threshold=0.05):
        """Prune memories below strength threshold. Called during dream mode."""
        pruned = []
        for slot in list(self.memory.keys()):
            if self._strength(slot) < threshold:
                del self.memory[slot]
                self.meta.pop(slot, None)
                pruned.append(slot)
        if pruned:
            np.save(self.path, self.memory)
            self._save_meta()
            print(f"[HIPPOCAMPUS] Pruned {len(pruned)} weak memories.")
        return pruned

    def all_slots(self):
        return list(self.memory.keys())

    def memory_report(self) -> dict:
        report = {}
        for slot in self.memory:
            report[slot] = {
                "strength": round(self._strength(slot), 3),
                "access_count": self.meta.get(slot, {}).get("access_count", 0),
                "stability_hours": round(self.meta.get(slot, {}).get("stability", 24.0), 1)
            }
        return report

    def similarity_search(self, query_vec, top_k=5):
        qf = query_vec.astype(np.float32)
        qn = np.linalg.norm(qf)
        if qn == 0:
            return []
        results = []
        for slot, vec in self.memory.items():
            if vec is None:
                continue
            strength = self._strength(slot)
            if strength < 0.01:
                continue
            vf = vec.astype(np.float32)
            vn = np.linalg.norm(vf)
            if vn == 0:
                continue
            # Similarity weighted by memory strength
            sim = float(np.dot(qf, vf) / (qn * vn)) * strength
            results.append((sim, slot))
        results.sort(reverse=True)
        return results[:top_k]
