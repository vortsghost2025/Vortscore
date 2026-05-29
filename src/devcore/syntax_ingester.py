import ast
import os
import json

class SyntaxIngester:
    def __init__(self, output_dim=512):
        self.output_dim = output_dim

    def parse_file_to_ast(self, file_path):
        """Reads a local source file and parses it into an Abstract Syntax Tree."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Target file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
            
        try:
            return ast.parse(source_code)
        except SyntaxError as e:
            # Finesse means capturing semantic dissonance early
            print(f"[-] Syntax error encountered during parsing: {e}")
            return None

    def flatten_ast_structure(self, node):
        """Recursively flattens the AST into a highly structured logic sequence."""
        sequence = []
        for n in ast.walk(node):
            node_type = type(n).__name__
            
            # Extract structural identity based on node type
            if isinstance(n, ast.FunctionDef):
                sequence.append({"type": node_type, "identifier": n.name, "args": len(n.args.args)})
            elif isinstance(n, ast.ClassDef):
                sequence.append({"type": node_type, "identifier": n.name})
            elif isinstance(n, (ast.If, ast.While, ast.For)):
                sequence.append({"type": node_type, "gate_logic": "conditional_branch"})
            elif isinstance(n, ast.Name):
                sequence.append({"type": node_type, "id": n.id})
            elif isinstance(n, ast.operator):
                sequence.append({"type": "Operator", "op": node_type})
                
        return sequence

    def process_directory(self, dir_path):
        """Processes a target directory of clean codebase source files."""
        payload = []
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    tree = self.parse_file_to_ast(full_path)
                    if tree:
                        structural_profile = self.flatten_ast_structure(tree)
                        payload.append({
                            "source_file": file,
                            "profile": structural_profile
                        })
        return payload

if __name__ == "__main__":
    # Self-test the ingester on our own runtime modules
    ingester = SyntaxIngester()
    print("[+] Initializing system self-analysis baseline...")
    try:
        sample_profile = ingester.process_directory("src/devcore")
        print(f"[+] Ingestion complete. Parsed modules: {len(sample_profile)}")
        print(json.dumps(sample_profile[:1], indent=2))
    except Exception as e:
        print(f"[-] Self-test initialization failed: {e}")
