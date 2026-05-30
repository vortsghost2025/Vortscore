#!/usr/bin/env python3
"""
Dream Mode — Vitalis FSI Memory Consolidation Engine.
Runs during idle time. Strengthens important patterns.
Prunes weak memories. Merges similar vectors.
This is what makes the system get smarter without explicit training.
"""
import time
import os
import numpy as np
from src.hippocampus import Hippocampus
from vitalis_ide.math_core.kernel import VitalisKernel

IDLE_THRESHOLD = 30  # seconds of no tasks before dream starts

class DreamEngine:
    def __init__(self):
        self.hippocampus = Hippocampus()
        self.kernel = VitalisKernel()
        self.task_file = os.path.expanduser("~/vitalis_devcore/workspace_tasks.json")
        self.dream_log = os.path.expanduser("~/.vitalis_workspace/dream_log.json")
        self.cycles = 0

    def _system_idle(self) -> bool:
        if not os.path.exists(self.task_file):
            return True
        age = time.time() - os.path.getmtime(self.task_file)
        return age > IDLE_THRESHOLD

    def _consolidate(self):
        """Merge similar memory vectors to build stronger generalizations."""
        slots = self.hippocampus.all_slots()
        if len(slots) < 2:
            return 0
        merged = 0
        checked = set()
        for i, slot_a in enumerate(slots):
            if slot_a in checked:
                continue
            vec_a = self.hippocampus.recall(slot_a)
            if vec_a is None:
                continue
            for slot_b in slots[i+1:]:
                if slot_b in checked:
                    continue
                vec_b = self.hippocampus.recall(slot_b)
                if vec_b is None:
                    continue
                sim = self.kernel.similarity(vec_a, vec_b)
                # Merge very similar memories into one stronger pattern
                if sim > 0.92:
                    bundle = np.sign(
                        vec_a.astype(np.int32) + vec_b.astype(np.int32)
                    ).astype(np.int8)
                    bundle[bundle == 0] = 1
                    self.hippocampus.store(slot_a, bundle)
                    checked.add(slot_b)
                    merged += 1
        return merged

    def run(self):
        print("[DREAM] Memory consolidation engine online.")
        while True:
            if self._system_idle():
                print(f"[DREAM] Cycle {self.cycles + 1} — consolidating...")
                pruned = self.hippocampus.forget_weak(threshold=0.03)
                merged = self._consolidate()
                report = self.hippocampus.memory_report()
                active = sum(1 for v in report.values() if v["strength"] > 0.5)
                self.cycles += 1
                print(f"[DREAM] Complete — Active:{active} Pruned:{len(pruned)} Merged:{merged}")
            time.sleep(60)

if __name__ == "__main__":
    DreamEngine().run()
