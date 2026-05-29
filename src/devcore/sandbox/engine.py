
import json
import os

class StateEngine:
    def __init__(self, file='data.json'):
        self.file = file
    
    def run(self):
        count = 0
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                count = json.load(f).get('count', 0)
        
        count += 1
        with open(self.file, 'w') as f:
            json.dump({'count': count}, f)
        return f"Count is {count}"
