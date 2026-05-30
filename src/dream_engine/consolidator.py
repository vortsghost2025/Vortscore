"""
DreamEngine — Vitalis FSI

Runs during idle time. Clusters recent hypervectors,
compresses them into HelixMemory prototypes.
This is how Vitalis consolidates experience into long-term patterns.
No external dependencies. Pure HDC clustering.
"""
import numpy as np
from collections import deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
from src.dream_engine.helix_memory import HelixMemory


class DreamEngine:
    DREAM_INTERVAL_MINUTES = 30
    MIN_BUFFER_SIZE = 50
    N_CLUSTERS = 4
    CLUSTER_ITERATIONS = 8

    def __init__(
        self,
        helix: HelixMemory,
        buffer_max: int = 500,
    ):
        self.helix = helix
        self.buffer: deque = deque(maxlen=buffer_max)
        self.last_dream: datetime = datetime.min
        self.dream_count: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def ingest(self, hv: np.ndarray, meta: Optional[dict] = None) -> None:
        """Accept one hypervector into the episodic buffer."""
        self.buffer.append((datetime.utcnow(), hv, meta or {}))

    def dream(self, force: bool = False) -> bool:
        """
        Consolidate episodic buffer into HelixMemory.
        Returns True if consolidation ran, False if skipped.
        """
        now = datetime.utcnow()
        if not force:
            if (now - self.last_dream) < timedelta(minutes=self.DREAM_INTERVAL_MINUTES):
                return False
        if len(self.buffer) < self.MIN_BUFFER_SIZE:
            print(f"[DREAM] Buffer too small ({len(self.buffer)}). Skipping.")
            return False

        print(f"[DREAM] Consolidating {len(self.buffer)} vectors...")

        # Extract hypervectors and metadata
        hvs = np.stack([hv for _, hv, _ in self.buffer]).astype(np.int8)
        metas = [meta for _, _, meta in self.buffer]

        # Cluster
        centroids, assignments = self._cluster(hvs)

        # Store each centroid as a helix code
        consolidated = 0
        for i, centroid in enumerate(centroids):
            cluster_mask = assignments == i
            if not np.any(cluster_mask):
                continue
            # Aggregate metadata from this cluster
            cluster_metas = [metas[j] for j in range(len(metas)) if cluster_mask[j]]
            merged_meta = self._merge_meta(cluster_metas)
            merged_meta["cluster_size"] = int(np.sum(cluster_mask))
            merged_meta["dream_cycle"] = self.dream_count
            self.helix.add(centroid, merged_meta)
            consolidated += 1

        # Generative replay — re-ingest perturbed versions of rare patterns
        self._replay(hvs, assignments)

        # Clean up
        self.buffer.clear()
        self.last_dream = now
        self.dream_count += 1
        print(f"[DREAM] Cycle {self.dream_count} complete. "
              f"{consolidated} prototypes stored in HelixMemory.")
        return True

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------
    def _cluster(
        self, hvs: np.ndarray
    ):
        """
        Online bipolar k-means.
        Distance metric: Hamming (count of differing bits).
        Centroids are binarized after each update.
        """
        k = min(self.N_CLUSTERS, len(hvs))
        indices = np.random.choice(len(hvs), k, replace=False)
        centroids = hvs[indices].copy().astype(np.int8)

        assignments = np.zeros(len(hvs), dtype=np.int32)
        for _ in range(self.CLUSTER_ITERATIONS):
            # Hamming distance: count positions where they differ
            diffs = np.stack(
                [np.sum(hvs != c, axis=1) for c in centroids],
                axis=1
            )
            assignments = np.argmin(diffs, axis=1)

            # Update centroids via majority vote (bipolar sign)
            for i in range(k):
                mask = assignments == i
                if np.any(mask):
                    summed = hvs[mask].astype(np.int32).sum(axis=0)
                    new_centroid = np.sign(summed).astype(np.int8)
                    new_centroid[new_centroid == 0] = 1
                    centroids[i] = new_centroid

        return centroids, assignments

    def _replay(self, hvs: np.ndarray, assignments: np.ndarray) -> None:
        """
        Generative replay: add small noise to rare cluster members
        and re-ingest them. Prevents forgetting of low-frequency patterns.
        """
        cluster_sizes = np.bincount(assignments, minlength=self.N_CLUSTERS)
        rare_threshold = np.percentile(cluster_sizes, 25)

        for i, size in enumerate(cluster_sizes):
            if size <= rare_threshold and size > 0:
                rare_hvs = hvs[assignments == i]
                for hv in rare_hvs[:2]:  # replay at most 2 per rare cluster
                    noise = np.random.choice(
                        [-1, 1],
                        size=len(hv),
                        p=[0.02, 0.98]
                    ).astype(np.int8)
                    perturbed = (hv * noise).astype(np.int8)
                    self.buffer.append((datetime.utcnow(), perturbed, {"replayed": True}))

    @staticmethod
    def _merge_meta(metas: list) -> dict:
        """Merge a list of metadata dicts into one summary."""
        merged = {}
        for m in metas:
            for k, v in m.items():
                if k not in merged:
                    merged[k] = v
        return merged
