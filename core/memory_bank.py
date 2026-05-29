import json, time, os

class MemoryBank:
    def __init__(self, storage_path="vitalis_memory.json"):
        self.storage_path = os.path.abspath(storage_path)
        
    def record_event(self, event_type, data):
        memory = {}
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    memory = json.load(f)
            except json.JSONDecodeError:
                pass # Ignore corruption, overwrite with new memory
        
        timestamp = str(time.time())
        memory[timestamp] = {"type": event_type, "payload": data}
        
        with open(self.storage_path, 'w') as f:
            json.dump(memory, f, indent=2)
