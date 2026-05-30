import numpy as np
from pathlib import Path
import ast
import hdc_engine

DIM = 10000

class VitalisKernel:
    def __init__(self):
        self.dim = DIM
        self.weights_path = Path.home() / ".vitalis_workspace" / "kernel.weights.npy"
        self.codebook_path = Path.home() / ".vitalis_workspace" / "codebook.npy"
        self.bias = np.load(self.weights_path) if self.weights_path.exists() else np.array([0.0])
        self._load_codebook()

    def _load_codebook(self):
        if self.codebook_path.exists():
            self.codebook = np.load(self.codebook_path, allow_pickle=True).item()
        else:
            self.codebook = {}

    def _save_codebook(self):
        self.codebook_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(self.codebook_path, self.codebook)

    def _get_token_vector(self, token: str) -> np.ndarray:
        if token not in self.codebook:
            self.codebook[token] = np.random.choice(
                [-1, 1], size=self.dim
            ).astype(np.int8)
            self._save_codebook()
        return self.codebook[token]

    def _get_position_vector(self, position: int) -> np.ndarray:
        rng = np.random.default_rng(seed=position)
        return rng.choice([-1, 1], size=self.dim).astype(np.int8)

    def vectorize_tokens(self, tokens: list, positional: bool = True) -> np.ndarray:
        bundle = np.zeros(self.dim, dtype=np.int32)
        for i, token in enumerate(tokens):
            token_vec = self._get_token_vector(str(token))
            if positional:
                pos_vec = self._get_position_vector(i)
                bound = hdc_engine.bind(token_vec, pos_vec)
            else:
                bound = token_vec
            bundle += bound.astype(np.int32)
        result = np.sign(bundle).astype(np.int8)
        result[result == 0] = 1
        return result

    def vectorize_source(self, source_code: str) -> np.ndarray:
        tokens = self._extract_tokens(source_code)
        return self.vectorize_tokens(tokens)

    def vectorize_file(self, file_path: str) -> np.ndarray:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")
        return self.vectorize_source(path.read_text(encoding="utf-8"))

    def _extract_tokens(self, source_code: str) -> list:
        tokens = []
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    tokens.append(f"DEF:{node.name}")
                elif isinstance(node, ast.Name):
                    tokens.append(f"NAME:{node.id}")
                elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                    tokens.append(f"STR:{node.value[:32]}")
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        tokens.append(f"IMPORT:{alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    tokens.append(f"FROM:{node.module}")
        except SyntaxError:
            tokens = source_code.split()
        return tokens if tokens else ["EMPTY"]

    def similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        a = vec_a.astype(np.float32)
        b = vec_b.astype(np.float32)
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        if denom == 0:
            return 0.0
        return float(np.dot(a, b) / denom)

    def matmul(self, a, b):
        return np.dot(a, b) + self.bias

    def activation(self, x):
        return np.sign(x)
