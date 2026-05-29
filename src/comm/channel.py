#!/usr/bin/env python3
from collections import defaultdict
from typing import Callable, Any, Dict, List

class Channel:
    """
    Central Message Bus.
    Components publish events (e.g., 'sensor_data', 'surprise_alert')
    and other components subscribe to those topics.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable):
        self._subscribers[topic].append(callback)

    def publish(self, topic: str, payload: Any):
        for callback in self._subscribers[topic]:
            callback(payload)

# Global singleton so all modules see the same bus
channel = Channel()
