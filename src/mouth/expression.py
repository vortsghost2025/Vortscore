#!/usr/bin/env python3
from src.comm.channel import channel
class Mouth:
    def execute_action(self, action: str):
        print(f"[MOUTH] Manifesting action: {action}")
        channel.publish("action_completed", action)
