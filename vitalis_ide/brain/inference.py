from vitalis_ide.brain.ledger import record
from vitalis_ide.brain.truth_manager import safe_response
from vitalis_ide.brain.rag import RAGEngine
from vitalis_ide.brain.bridge import ConfidenceBridge
from typing import Optional, Callable, Tuple, Dict, Any

class InferenceEngine:
    def __init__(self, model_fn: Optional[Callable[[str], Tuple[str, float]]] = None, use_rag: bool = True):
        self.model_fn = model_fn
        self.rag = RAGEngine() if use_rag else None
        self.bridge = ConfidenceBridge(self.rag) if self.rag else None

    def generate(self, prompt: str, explain: bool = False, record_entry: bool = True, tags: Optional[list] = None) -> Dict[str, Any]:
        # 1. Initial generation
        raw_answer, raw_confidence = self.model_fn(prompt) if self.model_fn else ("I don't know", 0.3)
        
        # 2. Autonomous Bridge Check
        if self.bridge and self.bridge.needs_augmentation(raw_confidence):
            augmented_prompt = self.bridge.bridge_query(prompt)
            raw_answer, raw_confidence = self.model_fn(augmented_prompt) if self.model_fn else ("I don't know", 0.3)

        # 3. Apply confidence guard
        filtered_answer, classification = safe_response(raw_answer, raw_confidence)
        
        # 4. Record to ledger
        entry_id = record(prompt=prompt, answer=filtered_answer, confidence=raw_confidence, tags=tags or []) if record_entry else ""

        return {"answer": filtered_answer, "confidence": raw_confidence, "classification": classification, "entry_id": entry_id}

    def generate_text(self, prompt: str, **kwargs) -> str:
        return self.generate(prompt, **kwargs)["answer"]
