"""
VitalisMind — The Cognitive Orchestrator

This is the unified cognitive layer.
Every task passes through here before execution.
The mind reasons, not just executes.
"""
import os
from src.cognition.identity import IdentityCore
from src.cognition.personality import PersonalityMatrix
from src.cognition.abstraction import AbstractionEngine
from src.cognition.reasoning import ReasoningEngine
from src.cognition.meta_rules import MetaRulesEngine
from src.brain.resonance import ResonanceEngine

class VitalisMind:
    def __init__(self):
        print("[MIND] Awakening cognitive systems...")
        self.identity    = IdentityCore()
        self.personality = PersonalityMatrix()
        self.abstraction = AbstractionEngine()
        self.reasoning   = ReasoningEngine()
        self.meta_rules  = MetaRulesEngine()
        self.resonance   = ResonanceEngine()
        self._session_actions = []
        print("[MIND] Cognitive layer online.")

    def process(self, intent: str, context: dict = None) -> dict:
        """
        Full cognitive cycle for a single task.
        1. Detect reasoning mode from context
        2. Check identity alignment
        3. Query meta-rules for known patterns
        4. Return enriched decision package
        """
        context = context or {}

        # 1. Reasoning mode
        mode = self.reasoning.detect_mode(intent)
        params = self.reasoning.get_params(mode)

        # 2. Identity alignment
        from vitalis_ide.math_core.kernel import VitalisKernel
        kernel = VitalisKernel()
        intent_vec = kernel.vectorize_tokens(intent.split(), positional=False)
        alignment = self.identity.alignment(intent_vec)

        # 3. Meta-rule match
        rule_match = self.meta_rules.match(intent)

        # 4. Personality influence
        profile = self.personality.profile()

        decision = {
            "intent": intent,
            "mode": mode,
            "alignment": round(alignment, 3),
            "confidence": round(
                alignment * 0.4 +
                self.resonance.get_weight(intent.split()[0] if intent else "unknown") * 0.3 +
                params["caution"] * 0.3, 3
            ),
            "params": params,
            "rule_match": rule_match,
            "personality": profile["character"],
            "dominant_trait": profile["dominant"],
        }

        self._session_actions.append(intent)
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

    def introspect(self) -> dict:
        """Full cognitive state report."""
        return {
            "identity_active": os.path.exists(
                os.path.expanduser("~/.vitalis_workspace/identity.npy")),
            "personality":     self.personality.profile(),
            "reasoning":       self.reasoning.report(),
            "meta_rules":      self.meta_rules.report(),
            "resonance":       self.resonance.report(),
        }
