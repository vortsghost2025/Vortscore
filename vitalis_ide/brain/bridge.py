"""
Bridge Module — Autonomous confidence recovery.
If confidence is in the hypothesis zone, this module forces a RAG retrieval
to boost context and re-evaluate.
"""

from vitalis_ide.brain.rag import RAGEngine

class ConfidenceBridge:
    def __init__(self, rag_engine: RAGEngine):
        self.rag = rag_engine

    def needs_augmentation(self, confidence: float) -> bool:
        # Range 0.45 to 0.65 triggers the Bridge
        return 0.45 <= confidence < 0.65

    def bridge_query(self, prompt: str) -> str:
        # Augment existing prompt with fresh RAG data
        return self.rag.augment_prompt(prompt, k=5)
