#!/usr/bin/env python3
import random
from src.energy.water_precision import get_precision

FREE_ENERGY_MAX = 2.5
PRECISION_MIN = 0.35

_UNKNOWN_RESPONSES = [
    "I don’t know the answer to that yet.",
    "I’m still learning about this topic.",
    "Sorry, I haven’t seen that before.",
    "That’s outside my current knowledge – I’ll keep learning."
]

def should_answer(free_energy: float) -> bool:
    return (free_energy < FREE_ENERGY_MAX) and (get_precision() > PRECISION_MIN)

def safe_response(free_energy: float, raw_output: str) -> str:
    if should_answer(free_energy):
        return raw_output.strip()
    return random.choice(_UNKNOWN_RESPONSES)
