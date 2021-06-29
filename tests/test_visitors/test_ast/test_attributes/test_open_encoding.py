import pytest

from wemake_python_styleguide.violations.best_practices import (
    UnspecifiedEncodingViolation,
)
from wemake_python_styleguide.visitors.ast.attributes import EncodingVisitor

unspecified_encoding_with = """
with open('filename.txt') as fd:
    fd.read()
"""

specified_encoding_with = """
with open('filename.txt', encoding='ascii') as fd:
    fd.read()
"""

unspecified_encoding_assign = """
file = open('filename.txt', 'r')
"""

specified_encoding_assign = """
file = open('filename.txt', 'r', encoding='utf8')
"""

specified_encoding_with_none = """
with open('filename.txt', encoding=None) as fd:
    fd.read()
"""

unspecified_encoding_with_multiple = """
with open('filename.txt', 'w', -1) as fd:
    fd.read()
"""

specified_encoding_with_multiple = """
with open('filename.txt', 'w', -1, None) as fd:
    fd.read()
"""

unspecified_encoding_assign_multiple = """
file = open('filename.txt', 'w', -1)
"""

specified_encoding_assign_multiple = """
file = open('filename.txt', 'w', -1, None)
"""


@pytest.mark.parametrize('code', [
    unspecified_encoding_with,
    unspecified_encoding_assign,
    unspecified_encoding_with_multiple,
    unspecified_encoding_assign_multiple,
])
def test_unspecified_encoding(
    assert_errors,
    code,
    default_options,
    parse_ast_tree,
):
    """Testing open encoding is unspecified."""
    tree = parse_ast_tree(code)
    visitor = EncodingVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnspecifiedEncodingViolation])


@pytest.mark.parametrize('code', [
    specified_encoding_with,
    specified_encoding_assign,
    specified_encoding_with_none,
    specified_encoding_with_multiple,
    specified_encoding_assign_multiple,
])
def test_specified_encoding(
    assert_errors,
    code,
    default_options,
    parse_ast_tree,
):
    """Testing open encoding is specified."""
    tree = parse_ast_tree(code)
    visitor = EncodingVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
