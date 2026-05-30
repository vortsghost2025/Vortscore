#!/usr/bin/env python3
"""
Dream Mode — Memory consolidation + abstraction formation.
The system thinks while it sleeps.
"""
import time, os
import numpy as np
from src.hippocampus import Hippocampus
from vitalis_ide.math_core.kernel import VitalisKernel
from src.cognition.abstraction import AbstractionEngine

IDLE_THRESHOLD = 30

class DreamEngine:
    def __init__(self):
        self.hippocampus  = Hippocampus()
        self.kernel       = VitalisKernel()
        self.abstraction  = AbstractionEngine()
        self.task_file    = os.path.expanduser("~/vitalis_devcore/workspace_tasks.json")
        self.cycles       = 0

    def _system_idle(self):
        if not os.path.exists(self.task_file):
            return True
        return (time.time() - os.path.getmtime(self.task_file)) > IDLE_THRESHOLD

    def _consolidate(self):
        slots = self.hippocampus.all_slots()
        if len(slots) < 2:
            return 0
        merged, checked = 0, set()
        for i, slot_a in enumerate(slots):
            if slot_a in checked: continue
            vec_a = self.hippocampus.recall(slot_a)
            if vec_a is None: continue
            for slot_b in slots[i+1:]:
                if slot_b in checked: continue
                vec_b = self.hippocampus.recall(slot_b)
                if vec_b is None: continue
                if self.kernel.similarity(vec_a, vec_b) > 0.92:
                    merged_vec = np.sign(
                        vec_a.astype(np.int32) + vec_b.astype(np.int32)
                    ).astype(np.int8)
                    merged_vec[merged_vec == 0] = 1
                    self.hippocampus.store(slot_a, merged_vec)
                    checked.add(slot_b)
                    merged += 1
        return merged

    def run(self):
        print("[DREAM] Memory consolidation + abstraction engine online.")
        while True:
            if self._system_idle():
                print(f"[DREAM] Cycle {self.cycles + 1} — entering consolidation...")
                pruned  = self.hippocampus.forget_weak(threshold=0.03)
                merged  = self._consolidate()
                formed  = self.abstraction.run_abstraction_cycle({})
                report  = self.hippocampus.memory_report()
                active  = sum(1 for v in report.values() if v["strength"] > 0.5)
                self.cycles += 1
                print(f"[DREAM] Complete — Active:{active} "
                      f"Pruned:{len(pruned)} Merged:{merged} "
                      f"Concepts formed:{len(formed)}")
            time.sleep(60)

if __name__ == "__main__":
    DreamEngine().run()
