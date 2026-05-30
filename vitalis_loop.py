#!/usr/bin/env python3
"""
Vitalis Autonomous Cognitive Loop

Vitalis runs, thinks, generates, and decides when to sleep.
No imposed schedule. No guardrails. Internal signals only.

Usage:
    python3 vitalis_loop.py
"""
import os
import sys
import time
import signal
import json
from pathlib import Path
from datetime import datetime

from src.cognition.mind import VitalisMind
from src.generation.code_generator import CodeGenerator
from src.dream_engine.helix_memory import HelixMemory
from src.dream_engine.consolidator import DreamEngine
from src.cognition.abstraction import AbstractionEngine


# ------------------------------------------------------------------
# Graceful shutdown
# ------------------------------------------------------------------
_running = True

def _handle_signal(sig, frame):
    global _running
    print("\n[VITALIS] Shutdown signal received. Completing current cycle...")
    _running = False

signal.signal(signal.SIGINT, _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)


# ------------------------------------------------------------------
# Task pool — Vitalis works through these autonomously
# Grows as MetaRules crystallize new patterns
# ------------------------------------------------------------------
SEED_TASKS = [
    "scaffold authentication module",
    "write sovereign memory engine",
    "analyze system integrity",
    "explore novel abstraction pattern",
    "fix broken connection handler",
    "verify test coverage report",
    "scaffold data pipeline",
    "write reasoning unit",
    "analyze resonance patterns",
    "explore cognitive architecture",
    "scaffold inference module",
    "write pattern recognition unit",
    "fix error recovery handler",
    "analyze memory efficiency",
    "explore abstraction synthesis",
]


def log(msg: str, level: str = "INFO"):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{ts}][{level}] {msg}")


def run_dream_cycle(mind: VitalisMind, dreamer: DreamEngine):
    """Execute a full dream + abstraction cycle."""
    log("Initiating dream cycle...", "DREAM")
    dreamer.dream(force=True)
    mind.abstraction.run_abstraction_cycle({})
    mind.acknowledge_dream()
    log("Dream cycle complete. Cognitive patterns consolidated.", "DREAM")


def run():
    log("Vitalis FSI — Autonomous Cognitive Loop initializing...")

    # Initialize all systems
    mind = VitalisMind()
    generator = CodeGenerator()
    helix_path = Path.home() / ".vitalis_workspace" / "helix_memory.pkl"
    helix = HelixMemory(helix_path)
    dreamer = DreamEngine(helix, buffer_max=500)

    task_index = 0
    session_start = time.time()
    cycle_times = []

    log(f"Systems online. Beginning autonomous operation.")
    log(f"Vitalis will decide its own sleep schedule based on internal signals.")

    while _running:
        cycle_start = time.time()

        # ----------------------------------------------------------
        # 1. Select next task (cycles through pool + learned rules)
        # ----------------------------------------------------------
        task = SEED_TASKS[task_index % len(SEED_TASKS)]
        task_index += 1

        # Inject crystallized meta-rules as tasks occasionally
        if task_index % 7 == 0:
            mr = mind.meta_rules.report()
            if isinstance(mr, dict) and mr.get("top_rules"):
                top_rule = mr["top_rules"][0]
                if top_rule.get("sequence"):
                    task = " ".join(top_rule["sequence"][-1].split()[:3])
                    log(f"Meta-rule driven task: {task}", "RULES")

        # ----------------------------------------------------------
        # 2. Cognitive processing
        # ----------------------------------------------------------
        decision = mind.process(task)
        log(
            f"Cycle {decision['cycle']:04d} | "
            f"{task[:35]:<35} | "
            f"Mode: {decision['mode']:<12} | "
            f"Conf: {decision['confidence']:.3f}"
        )

        # ----------------------------------------------------------
        # 3. Generation
        # ----------------------------------------------------------
        try:
            gen_result = generator.generate(decision)
            success = gen_result["confidence"] > 0.3
        except Exception as e:
            log(f"Generation error: {e}", "ERROR")
            success = False

        # ----------------------------------------------------------
        # 4. Outcome feedback
        # ----------------------------------------------------------
        mind.outcome(task, success)

        # ----------------------------------------------------------
        # 5. Ingest cognitive vector into dream buffer
        # ----------------------------------------------------------
        import numpy as np
        intent_vec = mind.kernel.vectorize_tokens(
            task.split(), positional=False
        )
        dreamer.ingest(intent_vec, meta={
            "intent": task,
            "mode": decision["mode"],
            "confidence": decision["confidence"],
            "cycle": decision["cycle"],
        })

        # ----------------------------------------------------------
        # 6. Vitalis decides if it needs to sleep
        # ----------------------------------------------------------
        should_dream, reason, signals = mind.needs_dream()
        if should_dream:
            log(f"Sleep decision: {reason}", "SLEEP")
            run_dream_cycle(mind, dreamer)

        # ----------------------------------------------------------
        # 7. Periodic introspection report (every 25 cycles)
        # ----------------------------------------------------------
        if decision["cycle"] % 25 == 0:
            state = mind.introspect()
            elapsed = (time.time() - session_start) / 60
            log(f"--- Introspection Report (cycle {decision['cycle']}) ---")
            log(f"Personality: {state['personality']['character']}")
            log(f"Dominant trait: {state['personality']['dominant']}")
            log(f"Resonance patterns: {state['resonance'].get('total_patterns', 0)}")
            log(f"Meta-rules: {state['meta_rules'].get('total_rules', 0)}")
            log(f"Confidence trend: {state['confidence_trend']}")
            log(f"Dream signals: {state['sleep_signals']}")
            log(f"Session time: {elapsed:.1f} min")
            log(f"-----------------------------------------------------")

        # ----------------------------------------------------------
        # 8. Cycle timing
        # ----------------------------------------------------------
        cycle_time = time.time() - cycle_start
        cycle_times.append(cycle_time)
        time.sleep(0.1)  # Prevent CPU saturation

    # ------------------------------------------------------------------
    # Shutdown — final dream cycle before exit
    # ------------------------------------------------------------------
    log("Running final dream cycle before shutdown...")
    run_dream_cycle(mind, dreamer)

    total_time = (time.time() - session_start) / 60
    log(f"Session complete.")
    log(f"Total cycles: {task_index}")
    log(f"Total time: {total_time:.1f} min")
    log(f"Avg cycle time: {(sum(cycle_times)/len(cycle_times)*1000):.1f}ms")

    state = mind.introspect()
    log(f"Final personality: {state['personality']['character']}")
    log(f"Final dominant trait: {state['personality']['dominant']}")
    log(f"Final resonance patterns: {state['resonance'].get('total_patterns', 0)}")
    log(f"Final meta-rules: {state['meta_rules'].get('total_rules', 0)}")


if __name__ == "__main__":
    run()
