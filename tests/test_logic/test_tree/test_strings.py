import ast

import pytest

from wemake_python_styleguide.logic.tree import strings


@pytest.mark.parametrize(
    ('code', 'expected_types'),
    [
        ('f"hello"', [ast.Constant]),
        ('f"{x}"', [ast.FormattedValue]),
        ('f"a{x}b"', [ast.Constant, ast.FormattedValue, ast.Constant]),
        ('f"{x:{width}}"', [ast.FormattedValue, ast.FormattedValue]),
    ],
)
def test_formatted_string_parts(
    parse_ast_tree,
    code: str,
    expected_types: list[type],
) -> None:
    """Yields every literal and placeholder part, including nested ones."""
    tree = parse_ast_tree(code)
    node = tree.body[0].value
    parts = list(strings.formatted_string_parts(node))
    assert [type(part) for part in parts] == expected_types
