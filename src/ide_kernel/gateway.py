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
