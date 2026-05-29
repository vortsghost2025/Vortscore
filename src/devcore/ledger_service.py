import hashlib
import json
import logging
from datetime import datetime

log = logging.getLogger("VitalisCore")

class LedgerService:
    def __init__(self, ledger_file="production_ledger.json"):
        self.ledger_file = ledger_file

    def record_merge(self, module_name: str, file_path: str):
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "module": module_name,
            "hash": file_hash
        }
        with open(self.ledger_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        log.info(f"LEGER_RECORDED: {module_name} with hash {file_hash}")
