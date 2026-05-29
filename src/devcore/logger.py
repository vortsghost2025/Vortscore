import json
import datetime
import os

class Logger:
    def __init__(self, log_file="src/devcore/logs/build.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log(self, level, source, message, context=None):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "level": level,
            "source": source,
            "message": message,
            "context": context or {}
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def query_errors(self):
        """Retrieves only error-level logs for the agent to analyze."""
        errors = []
        if not os.path.exists(self.log_file):
            return errors
        with open(self.log_file, "r") as f:
            for line in f:
                entry = json.loads(line)
                if entry["level"] == "ERROR":
                    errors.append(entry)
        return errors
