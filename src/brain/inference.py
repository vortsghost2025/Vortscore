from src.core.transformer_wrapper import TransformerWrapper as SovereignTransformer

class InferenceEngine:
    def __init__(self):
        self.model = SovereignTransformer()

    def generate_text(self, prompt, **kwargs):
        # Passes the prompt to the wrapped transformer
        return self.model.infer(prompt)
