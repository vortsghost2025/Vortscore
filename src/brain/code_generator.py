from src.brain.pattern_library import PatternLibrary

class CodeGenerator:
    TEMPLATES = {
        "class": 'class {name}:\n    def __init__(self):\n        pass\n\n    def run(self):\n        pass\n',
        "function": 'def {name}({args}):\n    """{doc}"""\n    pass\n',
        "test": 'import pytest\n\ndef test_{name}():\n    # Arrange\n    # Act\n    # Assert\n    assert True\n',
        "module": '"""\n{name} — Sovereign module\n"""\n__version__ = "0.1.0"\n',
    }

    # Tuned threshold based on HDC bundle dilution characteristics
    SIMILARITY_THRESHOLD = 0.05

    def __init__(self):
        self.library = PatternLibrary()

    def generate(self, intent, context=None):
        context = context or {}
        similar = self.library.retrieve(intent, top_k=1)
        if similar and similar[0][0] > self.SIMILARITY_THRESHOLD:
            sim = similar[0][0]
            meta = similar[0][1]
            print(f"[GENERATOR] Pattern retrieved (sim={sim:.4f}): {meta['intent']}")
            return meta["code"]
        # Template fallback
        name = context.get("name", intent.split()[-1] if intent.split() else "generated")
        if "test" in intent.lower():
            return self.TEMPLATES["test"].format(name=name)
        elif "class" in intent.lower():
            return self.TEMPLATES["class"].format(name=name)
        elif "function" in intent.lower():
            return self.TEMPLATES["function"].format(
                name=name, args="", doc=intent)
        return self.TEMPLATES["module"].format(name=name)

    def learn(self, intent, code, file_path=None):
        self.library.store(intent, code, file_path)
