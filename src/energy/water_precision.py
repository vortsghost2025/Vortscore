#!/usr/bin/env python3
from src.energy.atomic_core import AtomicCore
from src.comm.channel import channel

_core = AtomicCore()
_precision = 1.0

def _update_precision(_payload=None):
    global _precision
    _precision = _core.precision()

channel.subscribe("water_update", _update_precision)

def get_precision() -> float:
    return _precision
