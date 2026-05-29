import json

class ContextManager:
    def __init__(self, manifest_path="system_architecture_map.json"):
        self.path = manifest_path

    def update_manifest(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
        return True
