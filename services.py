from pathlib import Path
from memory_engine import MemoryEngine

EMBED_DIM = 768
_memory_engine = None

def get_memory_engine():
    global _memory_engine
    if _memory_engine is None:
        _memory_engine = MemoryEngine(dim=EMBED_DIM)
        if Path("data/memory_store").is_dir():
            _memory_engine.load("data/memory_store")
    return _memory_engine
