#!/usr/bin/env python3
import subprocess
class ActionExecutor:
    def run(self, cmd: str):
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
