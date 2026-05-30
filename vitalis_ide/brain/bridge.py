from src.brain.inference import InferenceEngine

class ConfidenceBridge:
    def __init__(self):
        self.engine = InferenceEngine()

    def evaluate(self, prompt: str) -> dict:
        result = self.engine.reason(prompt)
        return {"result": result, "status": "ok"}
