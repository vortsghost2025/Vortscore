import threading
from collections import defaultdict
from typing import Tuple

_lock = threading.Lock()
_default = (0.5, 0.5)
_mood_store: defaultdict[str, Tuple[float, float]] = defaultdict(lambda: _default)

def get_mood(client_id: str) -> Tuple[float, float]:
    with _lock: return _mood_store[client_id]

def set_mood(client_id: str, valence: float, arousal: float) -> None:
    with _lock: _mood_store[client_id] = (valence, arousal)
