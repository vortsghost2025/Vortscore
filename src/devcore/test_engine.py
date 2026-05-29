import os
import subprocess
import logging
import pathlib
import xml.etree.ElementTree as ET
import yaml
from typing import Tuple, Dict
from src.devcore.ledger_service import LedgerService

log = logging.getLogger("VitalisCore")

class TestEngine:
    def __init__(self, repo_root="src/devcore/sandbox/project_build"):
        self.repo_root = pathlib.Path(repo_root).resolve()
        self.tests_dir = self.repo_root / "tests"
        self.reports_dir = self.repo_root / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.policy_path = "cde_policy.yaml"
        self.ledger = LedgerService()

    def load_policy(self):
        if os.path.exists(self.policy_path):
            with open(self.policy_path, "r") as f:
                return yaml.safe_load(f)
        return {"quality_gates": {"min_coverage": 80.0}}

    def run_tests(self, module_name: str) -> Tuple[bool, str, Dict[str, float]]:
        test_file = self.tests_dir / f"test_{module_name}.py"
        xml_report = self.reports_dir / f"{module_name}_results.xml"
        cmd = ["pytest", "-q", f"--junitxml={xml_report}", "--cov=src", str(test_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        metrics = {"tests_passed": 0, "tests_failed": 0, "coverage_percent": 0.0}
        if xml_report.exists():
            try:
                tree = ET.parse(xml_report)
                root = tree.getroot()
                metrics["tests_passed"] = len([c for c in root.iter("testcase") if c.find("failure") is None])
                metrics["tests_failed"] = len([c for c in root.iter("testcase") if c.find("failure") is not None])
            except:
                pass
        return result.returncode == 0, result.stdout, metrics

    def merge_to_production(self, module_name: str) -> bool:
        policy = self.load_policy()
        threshold = policy['quality_gates']['min_coverage']
        passed, output, metrics = self.run_tests(module_name)
        
        if passed and metrics.get("coverage_percent", 0) >= threshold:
            # Record the hash of the module before merging
            target_module = self.repo_root / "app" / f"{module_name}.py"
            self.ledger.record_merge(module_name, str(target_module))
            log.info(f"Policy satisfied for {module_name}. Proceeding to merge.")
            return True
        log.warning(f"Policy violation for {module_name}. Merge aborted.")
        return False
