import json, os, numpy as np, faiss
from pathlib import Path
from typing import Dict, List, Tuple, Any

class ConceptNode:
    def __init__(self, cid, label, embedding, confidence, edges=None):
        self.cid, self.label, self.embedding, self.confidence, self.edges = cid, label, embedding, confidence, edges or []
    def to_dict(self):
        return {"cid": self.cid, "label": self.label, "embedding": self.embedding.tolist(), "confidence": self.confidence, "edges": self.edges}
    @staticmethod
    def from_dict(d):
        return ConceptNode(int(d["cid"]), str(d["label"]), np.array(d["embedding"], dtype=np.float32), float(d["confidence"]), [tuple(e) for e in d.get("edges", [])])

class ConceptGraph:
    def __init__(self, dim=768, persist_dir="data/concept_graph"):
        self.dim, self.persist_dir = dim, Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.index = faiss.IndexFlatL2(dim)
        self._nodes: Dict[int, ConceptNode] = {}
    def add_node(self, label, embedding, confidence, edges=None):
        vec = embedding.astype(np.float32)
        vec /= np.linalg.norm(vec)
        self.index.add(np.expand_dims(vec, 0))
        cid = self.index.ntotal - 1
        node = ConceptNode(cid, label, vec, confidence, edges)
        self._nodes[cid] = node
        return cid
    def persist(self):
        with (self.persist_dir / "concepts.json").open("w") as f:
            json.dump([n.to_dict() for n in self._nodes.values()], f, indent=2)
        faiss.write_index(self.index, str(self.persist_dir / "faiss.index"))
