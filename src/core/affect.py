import re, string

_POS = {"great", "awesome", "fantastic", "good", "excellent", "optimal", "stable", "secure"}
_NEG = {"bad", "terrible", "awful", "hate", "horrible", "angry", "frustrated", "error", "fail"}
_HIGH_AROUSAL = {"!", "!!", "!!!"}
_LOW_AROUSAL = {"...", "…"}

def _clean(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation)).lower()

def extract_affect(text: str) -> tuple[float, float]:
    tokens = set(_clean(text).split())
    pos = len(tokens & _POS)
    neg = len(tokens & _NEG)
    
    sentiment = 0.0 if pos == neg == 0 else (pos - neg) / max(pos + neg, 1)
    valence = (sentiment + 1) / 2
    
    arousal = 0.5
    if any(p in text for p in _HIGH_AROUSAL): arousal = 0.9
    elif any(p in text for p in _LOW_AROUSAL): arousal = 0.2
    
    return round(valence, 3), round(arousal, 3)
