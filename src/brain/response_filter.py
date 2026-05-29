#!/usr/bin/env python3
from src.energy.atomic_core import AtomicCore
from src.brain.truth_manager import safe_response
from src.comm.channel import channel

class ResponseFilter:
    def __init__(self):
        self.core = AtomicCore()

    def handle(self, raw_text: str):
        free_energy = self.core.free_energy
        final_text = safe_response(free_energy, raw_text)
        channel.publish("assistant_reply", {"text": final_text})
