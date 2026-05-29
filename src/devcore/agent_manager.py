from src.devcore.template_factory import TemplateFactory

class DeveloperAgent:
    def autonomous_build_loop(self, task_name, description):
        print(f"[*] Agent invoked for: {task_name}")
        
        # STRICT DELEGATION:
        # Instead of the agent guessing code, we map the task description 
        # to a pre-validated template.
        if "audit" in description.lower():
            code = TemplateFactory.get_secure_template("audit")
        else:
            code = TemplateFactory.get_secure_template("default")
        
        path = f"src/devcore/sandbox/{task_name}.py"
        with open(path, "w") as f:
            f.write(code)
            
        return {"status": "success", "artifact": path}
