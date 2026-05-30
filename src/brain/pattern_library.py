import numpy as np
import os
import json
from src.hippocampus import Hippocampus
from vitalis_ide.math_core.kernel import VitalisKernel

class PatternLibrary:
    def __init__(self):
        self.root = os.path.expanduser("~/.vitalis_workspace")
        self.hdc = VitalisKernel()
        self.hippocampus = Hippocampus()
        self.meta_path = os.path.join(self.root, "pattern_meta.json")
        self._load_meta()

    def _load_meta(self):
        if os.path.exists(self.meta_path):
            with open(self.meta_path) as f:
                self.meta = json.load(f)
        else:
            self.meta = {}

    def _save_meta(self):
        os.makedirs(self.root, exist_ok=True)
        with open(self.meta_path, 'w') as f:
            json.dump(self.meta, f, indent=2)

    def store(self, intent: str, code: str, file_path: str = None):
        # Semantic encoding — no position binding
        vector = self.hdc.vectorize_tokens(intent.split(), positional=False)
        slot = f"pattern_{len(self.meta)}"
        self.hippocampus.store(slot, vector)
        self.meta[slot] = {"intent": intent, "code": code, "file": file_path}
        self._save_meta()
        print(f"[PATTERN] Learned: {intent} → slot {slot}")
        return slot

    def retrieve(self, query: str, top_k: int = 3) -> list:
        query_vec = self.hdc.vectorize_tokens(query.split(), positional=False)
        results = []
        for slot, meta in self.meta.items():
            vec = self.hippocampus.recall(slot)
            if vec is not None:
                sim = self.hdc.similarity(query_vec, vec)
                results.append((sim, meta))
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]
