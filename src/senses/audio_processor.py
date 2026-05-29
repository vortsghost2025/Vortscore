#!/usr/bin/env python3
from .base_sensor import BaseSensor
class AudioProcessor(BaseSensor):
    def sense(self):
        return "AUDIO_STREAM_INPUT"
