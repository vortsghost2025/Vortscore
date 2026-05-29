import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Tuple
import faiss
import numpy as np

def _ensure_numpy(vec: np.ndarray, dim: int) -> np.ndarray:
    if not isinstance(vec, np.ndarray): raise TypeError("Vector must be a numpy.ndarray")
    if vec.ndim != 1: raise ValueError("Vector must be 1-dimensional")
    if vec.shape[0] != dim: raise ValueError(f"Vector length {vec.shape[0]} does not match dim={dim}")
    return np.ascontiguousarray(vec.astype(np.float32))

class MemoryEngine:
    def __init__(self, dim: int, index_factory: str = "Flat", metric: str = "l2"):
        self.dim = dim
        self._lock = threading.RLock()
        self.metric = faiss.METRIC_L2 if metric == "l2" else faiss.METRIC_INNER_PRODUCT
        self.index = faiss.index_factory(dim, index_factory, self.metric)
        self._metadata: Dict[int, Dict[str, Any]] = {}

    def add(self, vector: np.ndarray, meta: Dict[str, Any] | None = None) -> int:
        vec = _ensure_numpy(vector, self.dim)
        with self._lock:
            self.index.add(np.expand_dims(vec, axis=0))
            new_id = self.index.ntotal - 1
            self._metadata[new_id] = meta or {}
            return new_id

    def query(self, vector: np.ndarray, k: int = 5) -> List[Tuple[int, float, Dict[str, Any]]]:
        vec = _ensure_numpy(vector, self.dim)
        with self._lock:
            distances, ids = self.index.search(np.expand_dims(vec, axis=0), k)
        return [(int(idx), float(dist), self._metadata.get(int(idx), {})) 
                for idx, dist in zip(ids[0], distances[0]) if idx != -1]

    def save(self, folder: str):
        path = Path(folder)
        path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path / "faiss.index"))
        with (path / "metadata.json").open("w") as f: json.dump(self._metadata, f)
