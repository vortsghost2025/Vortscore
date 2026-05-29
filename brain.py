import os
import sys
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.core.retrieval_engine import LocalRetrievalEngine

class MockInferenceStep:
    def __init__(self, operation, text, confidence, metadata):
        self.operation = operation
        self.text = text
        self.confidence = confidence
        self.metadata = metadata

def process_input(text, max_depth=12):
    retriever = LocalRetrievalEngine()
    matches = retriever.query(text, top_k=3)
    
    raw_steps = []
    if not matches:
        raw_steps.append(MockInferenceStep(
            operation="INITIALIZE",
            text="Autonomous core initialized. No contextual nodes found on disk.",
            confidence=1.0,
            metadata={"duration_ms": 15}
        ))
        class BaseNode:
            label = "System isolated. Awaiting operational ingestion data."
            confidence = 1.0
        return BaseNode(), raw_steps

    for idx, match in enumerate(matches):
        raw_steps.append(MockInferenceStep(
            operation="SELECT_PREMISE" if idx == 0 else "RESOLVE_RELATION",
            text=match.get('text', ''),
            confidence=match.get('alignment_score', 0.85),
            metadata={"duration_ms": 40 + (idx * 15), "source": match.get('source_path')}
        ))

    class FinalNode:
        label = matches[0].get('text', '')[:120] + "..."
        confidence = matches[0].get('alignment_score', 0.90)

    return FinalNode(), raw_steps

def get_ripple_payload(text, max_depth=12):
    final_node, raw_steps = process_input(text, max_depth=max_depth)
    step_payload = []
    
    for i, step in enumerate(raw_steps):
        sim_score = step.confidence
        sim_score = max(0.001, min(0.999, sim_score)) 
        calculated_loss = -math.log(sim_score) * 0.1
        
        step_payload.append({
            "id": i,
            "operation": step.operation,
            "confidence": float(step.confidence),
            "free_energy": float(calculated_loss),
            "duration_ms": int(step.metadata.get("duration_ms", 25)),
        })

    total_fe = sum(s["free_energy"] for s in step_payload)

    return {
        "steps": step_payload,
        "final_conclusion": {
            "label": final_node.label,
            "confidence": float(final_node.confidence),
        },
        "total_free_energy": total_fe,
    }
