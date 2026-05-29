from src.devcore.test_engine import TestEngine
import logging

log = logging.getLogger("VitalisCore")

class AutoDeveloper:
    def __init__(self):
        self.tester = TestEngine()

    def deploy_feature(self, module, code, intent):
        # 1. Generate tests
        self.tester.generate_tests(module, code)
        
        # 2. Run tests
        passed, output, metrics = self.tester.run_tests(module)
        
        if not passed or metrics["coverage_percent"] < 80.0:
            log.error(f"[!] Validation Failed: {module}")
            return False
            
        # 3. Merge
        return self.tester.merge_to_production(module)
