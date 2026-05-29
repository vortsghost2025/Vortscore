import ast

class SynthesisEngine:
    def __init__(self):
        # Deterministic Rules: The blueprint of your product logic.
        self.matrix = {
            "health_check": {
                "name": "check_system_status",
                "body": [ast.Return(value=ast.Constant(value="System Nominal"))]
            },
            "auth_flow": {
                "name": "authenticate_user",
                "args": ["user_id", "token"],
                "body": [ast.Return(value=ast.Constant(value=True))]
            }
        }

    def generate(self, intent):
        rule = self.matrix.get(intent)
        if not rule:
            return "def error(): return 'Invalid Intent'"

        # 1. Construct AST Node
        func = ast.FunctionDef(
            name=rule["name"],
            args=ast.arguments(
                posonlyargs=[], 
                args=[ast.arg(arg=a) for a in rule.get("args", [])],
                vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
            ),
            body=rule["body"],
            decorator_list=[]
        )

        # 2. Wrap in Module (required for proper unparsing)
        module = ast.Module(body=[func], type_ignores=[])

        # 3. Inject metadata (fix_missing_locations adds lineno/col_offset)
        ast.fix_missing_locations(module)
        
        # 4. Generate source code
        return ast.unparse(module)
