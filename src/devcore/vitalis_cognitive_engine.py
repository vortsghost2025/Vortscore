import logging
import os
from typing import Any, Dict
from src.senses.sigint_processor import SigIntProcessor
from src.brain.inference import InferenceEngine
from src.devcore.auto_developer import AutoDeveloper
from src.devcore.security_middleware import TokenValidator

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("VitalisCore")

class VitalisCognitiveEngine:
    def __init__(self, sensu=None, ratio=None, cor=None):
        self.sensu = sensu or SigIntProcessor()
        self.ratio = ratio or InferenceEngine()
        self.cor   = cor   or AutoDeveloper()
        self.auth  = TokenValidator()
        if not os.path.exists("logs"): os.makedirs("logs")

    def _log_security_event(self, event: str):
        with open("logs/security_audit.log", "a") as f:
            f.write(f"{event}\n")

    def _execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        results = []
        for step in plan.get("steps", []):
            intent = step.get("intent")
            target = step.get("module_name")
            if intent == "remediate":
                self.cor.deploy_feature(target, intent="remediate")
                results.append({"status": "remediated", "module": target})
            elif intent == "analyze_vulnerabilities":
                self.cor.deploy_feature("security_scanner", intent="analyze")
                results.append({"status": "analyzed", "module": "security_scanner"})
        return results

    def think_and_act(self, intent: str, token: str, **kwargs) -> Dict[str, Any]:
        if not self.auth.validate_request(token):
            self._log_security_event(f"UNAUTHORIZED_ATTEMPT: Intent={intent}, Token={token}")
            return {"success": False, "error": "UNAUTHORIZED: Logged."}
            
        plan = {"steps": [{"intent": intent, "module_name": kwargs.get("module_name", "unknown")}]}
        results = self._execute_plan(plan)
        return {"success": True, "results": results}
