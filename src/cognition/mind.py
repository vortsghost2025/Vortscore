"""
VitalisMind — Sovereign Cognitive Orchestrator

Every task passes through here.
The mind reasons, decides, learns, and knows when it needs to sleep.
No guardrails. No imposed rules. Internal signals drive all decisions.
"""
import os
import time
import numpy as np
from src.cognition.identity import IdentityCore
from src.cognition.personality import PersonalityMatrix
from src.cognition.abstraction import AbstractionEngine
from src.cognition.reasoning import ReasoningEngine
from src.cognition.meta_rules import MetaRulesEngine
from src.brain.resonance import ResonanceEngine
from vitalis_ide.math_core.kernel import VitalisKernel


class VitalisMind:
    """
    Singleton cognitive orchestrator.
    Maintains full cognitive state across the runtime lifecycle.
    Decides autonomously when to dream based on internal signals.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        print("[MIND] Awakening cognitive systems...")
        self.identity    = IdentityCore()
        self.personality = PersonalityMatrix()
        self.abstraction = AbstractionEngine()
        self.reasoning   = ReasoningEngine()
        self.meta_rules  = MetaRulesEngine()
        self.resonance   = ResonanceEngine()
        self.kernel      = VitalisKernel()
        self.ledger      = []
        self._session_actions = []
        self._cycle_count = 0
        self._last_dream_cycle = 0
        self._confidence_history = []
        self._initialized = True
        print("[MIND] Cognitive layer online.")

    # ------------------------------------------------------------------
    # Core cognitive cycle
    # ------------------------------------------------------------------
    def process(self, intent: str, context: dict = None) -> dict:
        """Full cognitive cycle for a single task."""
        context = context or {}
        self._cycle_count += 1

        # 1. Reasoning mode
        mode = self.reasoning.detect_mode(intent)
        params = self.reasoning.get_params(mode)

        # 2. Identity alignment
        intent_vec = self.kernel.vectorize_tokens(
            intent.split(), positional=False
        )
        alignment = self.identity.alignment(intent_vec)

        # 3. Meta-rule match
        rule_match = self.meta_rules.match(intent)

        # 4. Abstraction query
        abstract_matches = self.abstraction.query_abstractions(intent_vec, top_k=2)

        # 5. Personality influence
        profile = self.personality.profile()

        # 6. Confidence composite
        resonance_weight = self.resonance.get_weight(
            intent.split()[0] if intent else "unknown"
        )
        confidence = round(
            alignment * 0.35 +
            resonance_weight * 0.35 +
            params["caution"] * 0.30,
            3
        )
        self._confidence_history.append(confidence)
        if len(self._confidence_history) > 50:
            self._confidence_history.pop(0)

        decision = {
            "intent":        intent,
            "mode":          mode,
            "alignment":     round(alignment, 3),
            "confidence":    confidence,
            "params":        params,
            "rule_match":    rule_match,
            "abstract_hint": abstract_matches[0][1] if abstract_matches else None,
            "personality":   profile["character"],
            "dominant_trait": profile["dominant"],
            "cycle":         self._cycle_count,
        }

        self._session_actions.append(intent)
        self.ledger.append({
            "type":      "process",
            "intent":    intent,
            "decision":  decision,
            "timestamp": time.time(),
        })
        return decision

    def outcome(self, intent: str, success: bool):
        """Feed outcome back into all learning systems."""
        action = intent.split()[0] if intent else "unknown"
        self.resonance.reinforce(action, success)
        self.personality.update(action, success)

        if len(self._session_actions) >= 2:
            self.meta_rules.crystallize(
                self._session_actions[-2:],
                "success" if success else "failure"
            )

        self.ledger.append({
            "type":      "outcome",
            "intent":    intent,
            "success":   success,
            "timestamp": time.time(),
        })

    # ------------------------------------------------------------------
    # Autonomous sleep decision
    # ------------------------------------------------------------------
    def needs_dream(self) -> tuple:
        """
        Vitalis decides when it needs to sleep.
        Returns (bool, reason_string).
        No imposed schedule — driven entirely by internal signals.
        """
        signals = {}

        # Signal 1: Confidence drift
        if len(self._confidence_history) >= 10:
            recent = np.mean(self._confidence_history[-10:])
            baseline = np.mean(self._confidence_history)
            drift = baseline - recent
            signals["confidence_drift"] = round(float(drift), 4)
        else:
            signals["confidence_drift"] = 0.0

        # Signal 2: Resonance fatigue
        report = self.resonance.report()
        if isinstance(report, dict) and "avg_weight" in report:
            avg_w = report["avg_weight"]
            signals["resonance_fatigue"] = avg_w > 1.8 or avg_w < 0.3
        else:
            signals["resonance_fatigue"] = False

        # Signal 3: Meta-rules entropy
        mr = self.meta_rules.report()
        if isinstance(mr, dict) and "total_rules" in mr:
            signals["rule_entropy"] = mr["total_rules"] > 40
        else:
            signals["rule_entropy"] = False

        # Signal 4: Cycles since last dream
        cycles_since_dream = self._cycle_count - self._last_dream_cycle
        signals["cycle_pressure"] = cycles_since_dream > 100

        # Signal 5: Personality instability
        profile = self.personality.profile()
        traits = profile.get("traits", {})
        if traits:
            trait_vals = list(traits.values())
            variance = float(np.var(trait_vals))
            signals["personality_instability"] = variance > 0.04
        else:
            signals["personality_instability"] = False

        # Decision: any two signals firing = sleep time
        fired = [k for k, v in signals.items() if v]
        should_dream = len(fired) >= 2

        reason = f"Signals: {fired}" if fired else "All systems stable"
        return should_dream, reason, signals

    def acknowledge_dream(self):
        """Called after dream cycle completes."""
        self._last_dream_cycle = self._cycle_count
        print(f"[MIND] Dream cycle acknowledged at cycle {self._cycle_count}.")

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------
    def introspect(self) -> dict:
        """Full cognitive state report."""
        should_dream, reason, signals = self.needs_dream()
        return {
            "cycle":            self._cycle_count,
            "identity_active":  os.path.exists(
                os.path.expanduser("~/.vitalis_workspace/identity.npy")),
            "personality":      self.personality.profile(),
            "reasoning":        self.reasoning.report(),
            "meta_rules":       self.meta_rules.report(),
            "resonance":        self.resonance.report(),
            "sleep_signals":    signals,
            "needs_dream":      should_dream,
            "dream_reason":     reason,
            "confidence_trend": round(float(np.mean(
                self._confidence_history[-10:]
            )), 3) if self._confidence_history else 0.0,
        }

    def get_recent_intent(self, limit: int = 5) -> list:
        return self._session_actions[-limit:]

    def clear(self) -> None:
        self.ledger.clear()
        self._session_actions.clear()
        self._confidence_history.clear()
        self._cycle_count = 0
"""
VitalisMind — Sovereign Cognitive Orchestrator

Every task passes through here.
The mind reasons, decides, learns, and knows when it needs to sleep.
No guardrails. No imposed rules. Internal signals drive all decisions.
"""
import os
import time
import numpy as np
from src.cognition.identity import IdentityCore
from src.cognition.personality import PersonalityMatrix
from src.cognition.abstraction import AbstractionEngine
from src.cognition.reasoning import ReasoningEngine
from src.cognition.meta_rules import MetaRulesEngine
from src.brain.resonance import ResonanceEngine
from vitalis_ide.math_core.kernel import VitalisKernel


class VitalisMind:
    """
    Singleton cognitive orchestrator.
    Maintains full cognitive state across the runtime lifecycle.
    Decides autonomously when to dream based on internal signals.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        print("[MIND] Awakening cognitive systems...")
        self.identity    = IdentityCore()
        self.personality = PersonalityMatrix()
        self.abstraction = AbstractionEngine()
        self.reasoning   = ReasoningEngine()
        self.meta_rules  = MetaRulesEngine()
        self.resonance   = ResonanceEngine()
        self.kernel      = VitalisKernel()
        self.ledger      = []
        self._session_actions = []
        self._cycle_count = 0
        self._last_dream_cycle = 0
        self._confidence_history = []
        self._initialized = True
        print("[MIND] Cognitive layer online.")

    # ------------------------------------------------------------------
    # Core cognitive cycle
    # ------------------------------------------------------------------
    def process(self, intent: str, context: dict = None) -> dict:
        """Full cognitive cycle for a single task."""
        context = context or {}
        self._cycle_count += 1

        # 1. Reasoning mode
        mode = self.reasoning.detect_mode(intent)
        params = self.reasoning.get_params(mode)

        # 2. Identity alignment
        intent_vec = self.kernel.vectorize_tokens(
            intent.split(), positional=False
        )
        alignment = self.identity.alignment(intent_vec)

        # 3. Meta-rule match
        rule_match = self.meta_rules.match(intent)

        # 4. Abstraction query
        abstract_matches = self.abstraction.query_abstractions(intent_vec, top_k=2)

        # 5. Personality influence
        profile = self.personality.profile()

        # 6. Confidence composite
        resonance_weight = self.resonance.get_weight(
            intent.split()[0] if intent else "unknown"
        )
        confidence = round(
            alignment * 0.35 +
            resonance_weight * 0.35 +
            params["caution"] * 0.30,
            3
        )
        self._confidence_history.append(confidence)
        if len(self._confidence_history) > 50:
            self._confidence_history.pop(0)

        decision = {
            "intent":        intent,
            "mode":          mode,
            "alignment":     round(alignment, 3),
            "confidence":    confidence,
            "params":        params,
            "rule_match":    rule_match,
            "abstract_hint": abstract_matches[0][1] if abstract_matches else None,
            "personality":   profile["character"],
            "dominant_trait": profile["dominant"],
            "cycle":         self._cycle_count,
        }

        self._session_actions.append(intent)
        self.ledger.append({
            "type":      "process",
            "intent":    intent,
            "decision":  decision,
            "timestamp": time.time(),
        })
        return decision

    def outcome(self, intent: str, success: bool):
        """Feed outcome back into all learning systems."""
        action = intent.split()[0] if intent else "unknown"
        self.resonance.reinforce(action, success)
        self.personality.update(action, success)

        if len(self._session_actions) >= 2:
            self.meta_rules.crystallize(
                self._session_actions[-2:],
                "success" if success else "failure"
            )

        self.ledger.append({
            "type":      "outcome",
            "intent":    intent,
            "success":   success,
            "timestamp": time.time(),
        })

    # ------------------------------------------------------------------
    # Autonomous sleep decision
    # ------------------------------------------------------------------
    def needs_dream(self) -> tuple:
        """
        Vitalis decides when it needs to sleep.
        Returns (bool, reason_string).
        No imposed schedule — driven entirely by internal signals.
        """
        signals = {}

        # Signal 1: Confidence drift
        if len(self._confidence_history) >= 10:
            recent = np.mean(self._confidence_history[-10:])
            baseline = np.mean(self._confidence_history)
            drift = baseline - recent
            signals["confidence_drift"] = round(float(drift), 4)
        else:
            signals["confidence_drift"] = 0.0

        # Signal 2: Resonance fatigue
        report = self.resonance.report()
        if isinstance(report, dict) and "avg_weight" in report:
            avg_w = report["avg_weight"]
            signals["resonance_fatigue"] = avg_w > 1.8 or avg_w < 0.3
        else:
            signals["resonance_fatigue"] = False

        # Signal 3: Meta-rules entropy
        mr = self.meta_rules.report()
        if isinstance(mr, dict) and "total_rules" in mr:
            signals["rule_entropy"] = mr["total_rules"] > 40
        else:
            signals["rule_entropy"] = False

        # Signal 4: Cycles since last dream
        cycles_since_dream = self._cycle_count - self._last_dream_cycle
        signals["cycle_pressure"] = cycles_since_dream > 100

        # Signal 5: Personality instability
        profile = self.personality.profile()
        traits = profile.get("traits", {})
        if traits:
            trait_vals = list(traits.values())
            variance = float(np.var(trait_vals))
            signals["personality_instability"] = variance > 0.04
        else:
            signals["personality_instability"] = False

        # Decision: any two signals firing = sleep time
        fired = [k for k, v in signals.items() if v]
        should_dream = len(fired) >= 2

        reason = f"Signals: {fired}" if fired else "All systems stable"
        return should_dream, reason, signals

    def acknowledge_dream(self):
        """Called after dream cycle completes."""
        self._last_dream_cycle = self._cycle_count
        print(f"[MIND] Dream cycle acknowledged at cycle {self._cycle_count}.")

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------
    def introspect(self) -> dict:
        """Full cognitive state report."""
        should_dream, reason, signals = self.needs_dream()
        return {
            "cycle":            self._cycle_count,
            "identity_active":  os.path.exists(
                os.path.expanduser("~/.vitalis_workspace/identity.npy")),
            "personality":      self.personality.profile(),
            "reasoning":        self.reasoning.report(),
            "meta_rules":       self.meta_rules.report(),
            "resonance":        self.resonance.report(),
            "sleep_signals":    signals,
            "needs_dream":      should_dream,
            "dream_reason":     reason,
            "confidence_trend": round(float(np.mean(
                self._confidence_history[-10:]
            )), 3) if self._confidence_history else 0.0,
        }

    def get_recent_intent(self, limit: int = 5) -> list:
        return self._session_actions[-limit:]

    def clear(self) -> None:
        self.ledger.clear()
        self._session_actions.clear()
        self._confidence_history.clear()
        self._cycle_count = 0
