#!/bin/bash
# 1. Patch src/ide_kernel/validator.py
cat << 'EOP' > src/ide_kernel/validator.py
import subprocess
import pathlib
from typing import Tuple

class KernelValidator:
    @staticmethod
    def run_tests(target_path: str) -> Tuple[bool, str]:
        test_dir = pathlib.Path(target_path) / "tests"
        if not test_dir.is_dir():
            return True, "No tests found."
        result = subprocess.run(["pytest", str(test_dir), "-q"], capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
EOP

# 2. Patch src/ide_kernel/gateway.py (Adding Pydantic Validation)
cat << 'EOP' > src/ide_kernel/gateway.py
from flask import Flask, request, jsonify
import json
import os
from pydantic import BaseModel, ValidationError, validator
from typing import Literal, Optional

app = Flask(__name__)
WORKSPACE = os.getcwd()
TASK_FILE = os.path.join(WORKSPACE, "workspace_tasks.json")

class TaskPayload(BaseModel):
    intent: Literal["scaffold", "write"]
    module_name: Optional[str] = None
    file: Optional[str] = None
    code: Optional[str] = None

@app.route('/execute', methods=['POST'])
def execute_task():
    try:
        data = TaskPayload.parse_obj(request.json or {})
    except ValidationError as exc:
        return jsonify({"error": exc.errors()}), 400
    with open(TASK_FILE, "w") as f:
        json.dump(data.dict(), f)
    return jsonify({"status": "Task Queued", "intent": data.intent}), 202
EOP

# 3. Patch src/devcore/vitalis_generator.py (Incremental)
cat << 'EOP' > src/devcore/vitalis_generator.py
import os
class VitalisGenerator:
    def __init__(self, staging_dir):
        self.staging_dir = staging_dir
    def write_to_staging(self, module_name: str, code_string: str) -> str:
        os.makedirs(self.staging_dir, exist_ok=True)
        module_path = os.path.join(self.staging_dir, f"{module_name}.py")
        with open(module_path, "w", encoding="utf-8") as f:
            f.write(code_string)
        return module_path
EOP

echo "[+] Architecture patches applied."
