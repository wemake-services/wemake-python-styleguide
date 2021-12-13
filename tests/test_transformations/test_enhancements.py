import pytest


@pytest.mark.parametrize(('expression', 'output'), [
    ('-1 + 1', 0),
    ('1 * 2', 2),
    ('"a" * 5', 'aaaaa'),
    ('b"hello" * 2', b'hellohello'),
    ('"hello " + "world"', 'hello world'),
    ('(2 + 6) / 4 - 2', 0),
    ('1 << 4', 16),
    ('255 >> 4', 15),
    ('2**4', 16),
    ('5^9', 12),
    ('12 & 24', 8),
    ('6 | 9', 15),
    ('5 % 3', 2),
    ('4 // 3', 1),
    ('(6 - 2) * ((3 << 3) // 10) % 5 | 7**2', 51),
])
def test_evaluate_valid_operations(parse_ast_tree, expression: str, output):
    """Tests that the operations are correctly evaluated."""
    tree = parse_ast_tree(expression)
    assert tree.body[0].value.wps_op_eval == output


@pytest.mark.parametrize('expression', [
    'x * 2',
    'x << y',
    '-x + y',
    '0 / 0',
    '"a" * 2.1',
    '"a" + 1',
    '3 << 1.5',
    '((4 - 1) * 3 - 9) // (7 >> 4)',
    '[[1, 0], [0, 1]] @ [[1, 1], [0, 0]]',
])
def test_evaluate_invalid_operations(parse_ast_tree, expression: str):
    """Tests that the operations can not be evaluated and thus return None."""
    tree = parse_ast_tree(expression)
    assert tree.body[0].value.wps_op_eval is None
