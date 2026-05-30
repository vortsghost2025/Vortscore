import time
import numpy as np
from vitalis_ide.math_core.kernel import VitalisKernel
from src.hippocampus import Hippocampus
from src.brain.pattern_library import PatternLibrary

print("\n╔══════════════════════════════════════╗")
print("║    VITALIS FSI — BENCHMARK SUITE    ║")
print("╚══════════════════════════════════════╝\n")

kernel = VitalisKernel()
hip = Hippocampus()
lib = PatternLibrary()

# 1. Vectorization speed
print("[1] VECTORIZATION SPEED")
tokens = "def authenticate user password hash verify token session".split()
runs = 100
t = time.time()
for _ in range(runs):
    kernel.vectorize_tokens(tokens)
elapsed = (time.time() - t) / runs * 1000
print(f"    {runs} vectors in {elapsed:.2f}ms avg per vector")
print(f"    Rating: {'FAST' if elapsed < 10 else 'ACCEPTABLE' if elapsed < 50 else 'SLOW'}\n")

# 2. Similarity accuracy
print("[2] SIMILARITY ACCURACY")
pairs = [
    ("authenticate user login", "user login authentication", True),
    ("write database query", "render html template", False),
    ("scaffold module class", "create new module structure", True),
]
correct = 0
for a, b, should_be_similar in pairs:
    va = kernel.vectorize_tokens(a.split())
    vb = kernel.vectorize_tokens(b.split())
    sim = kernel.similarity(va, vb)
    is_similar = sim > 0.3
    match = is_similar == should_be_similar
    correct += int(match)
    print(f"    '{a[:30]}' vs '{b[:30]}'")
    print(f"    sim={sim:.3f} | {'PASS' if match else 'FAIL'}")
print(f"    Accuracy: {correct}/{len(pairs)}\n")

# 3. Memory store/recall speed
print("[3] MEMORY STORE/RECALL SPEED")
vec = kernel.vectorize_tokens(["test", "vector"])
t = time.time()
for i in range(50):
    hip.store(f"bench_{i}", vec)
store_time = (time.time() - t) / 50 * 1000
t = time.time()
for i in range(50):
    hip.recall(f"bench_{i}")
recall_time = (time.time() - t) / 50 * 1000
print(f"    Store: {store_time:.2f}ms avg")
print(f"    Recall: {recall_time:.2f}ms avg")
print(f"    Total slots: {len(hip.all_slots())}\n")

# 4. Pattern retrieval accuracy
print("[4] PATTERN RETRIEVAL")
lib.store("write user authentication", "def auth(user, pwd): return True", "src/auth.py")
lib.store("scaffold database module", "# db module", "src/db/__init__.py")
lib.store("write unit test for router", "def test_route(): assert True", "tests/test_router.py")
results = lib.retrieve("user login auth", top_k=1)
if results:
    sim, meta = results[0]
    correct = "auth" in meta.get("file", "")
    print(f"    Query: 'user login auth'")
    print(f"    Retrieved: {meta.get('file')} (sim={sim:.3f})")
    print(f"    Result: {'PASS' if correct else 'FAIL'}\n")

print("╔══════════════════════════════════════╗")
print("║           BENCHMARK COMPLETE        ║")
print("╚══════════════════════════════════════╝\n")
