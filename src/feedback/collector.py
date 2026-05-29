#!/usr/bin/env python3
from src.comm.channel import channel
class FeedbackCollector:
    def report(self, result):
        channel.publish("feedback", {"status": result.returncode, "out": result.stdout})
