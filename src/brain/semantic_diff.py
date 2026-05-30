"""
Semantic Diff Engine.
Normal diff tells you WHAT changed.
This tells you WHAT IT MEANS that it changed.
"""
from vitalis_ide.math_core.kernel import VitalisKernel

class SemanticDiff:
    DRIFT_THRESHOLD = 0.3

    def __init__(self):
        self.kernel = VitalisKernel()

    def diff(self, code_before: str, code_after: str) -> dict:
        vec_before = self.kernel.vectorize_source(code_before)
        vec_after  = self.kernel.vectorize_source(code_after)
        similarity = self.kernel.similarity(vec_before, vec_after)
        drift = 1.0 - similarity

        if drift < 0.05:
            verdict = "TRIVIAL"
            description = "Cosmetic change only. Logic unchanged."
        elif drift < self.DRIFT_THRESHOLD:
            verdict = "MINOR"
            description = "Minor semantic shift. Core logic preserved."
        elif drift < 0.6:
            verdict = "SIGNIFICANT"
            description = "Significant semantic drift. Logic has changed."
        else:
            verdict = "BREAKING"
            description = "Near-complete semantic rewrite. Treat as new module."

        return {
            "similarity": round(similarity, 4),
            "drift": round(drift, 4),
            "verdict": verdict,
            "description": description,
        }

    def diff_files(self, path_before: str, path_after: str) -> dict:
        with open(path_before) as f: before = f.read()
        with open(path_after)  as f: after  = f.read()
        result = self.diff(before, after)
        result["files"] = {"before": path_before, "after": path_after}
        return result
