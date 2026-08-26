import ast
from pathlib import Path


def test_vitalis_mind_has_single_top_level_definition():
    mind_path = Path(__file__).parents[1] / "src" / "cognition" / "mind.py"
    tree = ast.parse(mind_path.read_text(encoding="utf-8"))

    definitions = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "VitalisMind"
    ]

    assert len(definitions) == 1
