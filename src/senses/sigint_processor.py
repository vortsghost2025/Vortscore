#!/usr/bin/env python3
from .base_sensor import BaseSensor
class SigIntProcessor(BaseSensor):
    def sense(self):
        return "SIGNAL_DETECTED"
