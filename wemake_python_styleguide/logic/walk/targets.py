import ast


def extract_names_from_targets(targets: list[ast.expr]) -> set[str]:
    """Extract names from delete statement targets."""
    names: set[str] = set()
    for target in targets:
        if isinstance(target, ast.Name):
            names.add(target.id)
    return names


def get_names_from_target(target: ast.expr) -> set[str]:
    """
    Extracts all variable names from a target expression.

    Works with simple names and unpacking, e.g.:
    - `for x in ...` -> {"x"}
    - `for x, y in ...` -> {"x", "y"}
    - `for (a, (b, c)) in ...` -> {"a", "b", "c"}
    """
    return {node.id for node in ast.walk(target) if isinstance(node, ast.Name)}
