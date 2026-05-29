class TemplateFactory:
    @staticmethod
    def get_secure_template(task_type):
        templates = {
            "audit": "import os\n# Structural Audit Script\nprint('Auditing directory...')\n",
            "fix": "def repair_module(path):\n    pass\n"
        }
        return templates.get(task_type, "# Default template\npass")
