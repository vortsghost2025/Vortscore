"""
AbstractionEngine — Vitalis FSI

The system doesn't just remember experiences.
It builds CONCEPTS from clusters of experiences.
This is the difference between memory and understanding.

Example:
  50 individual auth patterns →
  one abstract AUTH concept vector →
  faster retrieval, analogical reasoning, cross-domain transfer
"""
import numpy as np
import os
import json
from vitalis_ide.math_core.kernel import VitalisKernel
from src.hippocampus import Hippocampus

class AbstractionEngine:
    CLUSTER_THRESHOLD = 0.55
    MIN_CLUSTER_SIZE = 2

    def __init__(self):
        self.kernel = VitalisKernel()
        self.hippocampus = Hippocampus()
        self.path = os.path.expanduser("~/.vitalis_workspace/abstractions.json")
        self.abstract_path = os.path.expanduser("~/.vitalis_workspace/abstract_vectors.npy")
        self._load()

    def _load(self):
        self.abstractions = {}
        self.abstract_vectors = {}
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.abstractions = json.load(f)
        if os.path.exists(self.abstract_path):
            self.abstract_vectors = np.load(
                self.abstract_path, allow_pickle=True).item()

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'w') as f:
            json.dump(self.abstractions, f, indent=2)
        np.save(self.abstract_path, self.abstract_vectors)

    def abstract(self, vectors: dict) -> dict:
        """
        Takes a dict of {slot: vector}.
        Finds clusters. Builds concept vectors from each cluster.
        Returns {concept_name: abstract_vector}.
        """
        slots = list(vectors.keys())
        visited = set()
        concepts = {}

        for i, slot_a in enumerate(slots):
            if slot_a in visited:
                continue
            cluster = [slot_a]
            vec_a = vectors[slot_a]

            for slot_b in slots[i+1:]:
                if slot_b in visited:
                    continue
                vec_b = vectors[slot_b]
                sim = self.kernel.similarity(vec_a, vec_b)
                if sim > self.CLUSTER_THRESHOLD:
                    cluster.append(slot_b)
                    visited.add(slot_b)

            if len(cluster) >= self.MIN_CLUSTER_SIZE:
                # Bundle cluster into abstract concept
                bundle = np.zeros(self.kernel.dim, dtype=np.int32)
                for s in cluster:
                    bundle += vectors[s].astype(np.int32)
                concept_vec = np.sign(bundle).astype(np.int8)
                concept_vec[concept_vec == 0] = 1
                concept_name = f"concept_{len(concepts)}"
                concepts[concept_name] = {
                    "vector": concept_vec,
                    "members": cluster,
                    "size": len(cluster)
                }
                visited.add(slot_a)

        return concepts

    def run_abstraction_cycle(self, pattern_meta: dict) -> list:
        """
        Called during dream cycles.
        Takes current pattern library and forms higher-order concepts.
        """
        vectors = {}
        for slot in self.hippocampus.all_slots():
            vec = self.hippocampus.recall(slot)
            if vec is not None:
                vectors[slot] = vec

        if len(vectors) < self.MIN_CLUSTER_SIZE:
            return []

        new_concepts = self.abstract(vectors)
        formed = []
        for name, data in new_concepts.items():
            full_name = f"abstract_{len(self.abstractions)}_{name}"
            self.abstractions[full_name] = {
                "members": data["members"],
                "size": data["size"]
            }
            self.abstract_vectors[full_name] = data["vector"]
            formed.append(full_name)
            print(f"[ABSTRACTION] Concept formed: {full_name} ({data['size']} members)")

        if formed:
            self._save()
        return formed

    def query_abstractions(self, query_vec: np.ndarray, top_k: int = 3) -> list:
        """Search abstract concept space — faster than raw pattern search."""
        results = []
        for name, vec in self.abstract_vectors.items():
            sim = self.kernel.similarity(query_vec, vec)
            results.append((sim, name, self.abstractions.get(name, {})))
        results.sort(reverse=True)
        return results[:top_k]
