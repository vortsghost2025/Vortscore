import os

class IntegrationEngine:
    def __init__(self, project_root="src/devcore/sandbox/project_build"):
        self.entry_point = os.path.join(project_root, "app.py")

    def wire(self, module_name, function_name):
        # We need to make sure the app.py exists before we append
        if not os.path.exists(self.entry_point):
            with open(self.entry_point, "w") as f:
                f.write("from flask import Flask\napp = Flask(__name__)\n")
                
        with open(self.entry_point, "a") as f:
            f.write(f"\n\n# Dynamic Integration: {module_name}")
            f.write(f"\nfrom app.{module_name} import {function_name}")
            f.write(f"\napp.add_url_rule('/{module_name}', '{module_name}', {function_name}, methods=['POST'])")
        print(f"[+] INTEGRATED: '{module_name}' is now live at /api/{module_name}")
