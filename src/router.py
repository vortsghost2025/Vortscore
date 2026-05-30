from src.brain.inference import InferenceEngine

class Router:
    def __init__(self):
        self.engine = InferenceEngine()

    def route(self, prompt: str) -> str:
        return self.engine.reason(prompt)
