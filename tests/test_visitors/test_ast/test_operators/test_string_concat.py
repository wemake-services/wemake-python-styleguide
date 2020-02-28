import pytest

from wemake_python_styleguide.violations.consistency import (
    ExplicitStringConcatViolation,
)
from wemake_python_styleguide.visitors.ast.operators import (
    WrongMathOperatorVisitor,
)

usage_template = 'constant {0}'

docstring = """
def function():
    '''Docstring'''
    variable = 'a'
    format = 'some'.format(1)
"""

multiline_string_concat = """
long_text = (
    'first' +
    'second' +
    'third'
)
"""

multiline_bytes_concat = """
long_text = (
    b'first' +
    b'second' +
    b'third'
)
"""

multiline_format_concat = """
long_text = (
    f'first' +
    f'second' +
    f'third'
)
"""

multiline_mixed_concat = """
long_text = (
    'first' +
    b'second' +
    f'third'
)
"""


@pytest.mark.parametrize('expression', [
    '+ ""',
    "+ 'a'",
    '+ b"123"',
    '+ 1 + f""',
    '+ b"" + 2',

    '+= ""',
    "+= b'a'",
    '+= b"123"',
    '+= f""',
    '+= b""',
])
def test_string_concat(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that string concats are forbidden."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ExplicitStringConcatViolation])


@pytest.mark.parametrize('expression', [
    '- 1',
    '; x = "a" * 2',

    '*= 2',
])
def test_correct_operation(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that regular operations are allowed."""
    tree = parse_ast_tree(usage_template.format(expression))

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    docstring,
    multiline_string_concat,
    multiline_bytes_concat,
    multiline_format_concat,
    multiline_mixed_concat,
])
def test_correct_multiline_operation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that multiline string concat is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongMathOperatorVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
