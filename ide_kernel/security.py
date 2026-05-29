import yaml
import os

class CDEPolicyEnforcer:
    def __init__(self, policy_path="cde_policy.yaml"):
        self.policy_path = policy_path
        
    def check_task(self, task):
        if not os.path.exists(self.policy_path): return True
        with open(self.policy_path, 'r') as f:
            policy = yaml.safe_load(f)
        
        # Example Security Gate: Block dangerous intents
        if policy.get('security_strictness') == "high" and "delete" in str(task):
            return False
        return True
