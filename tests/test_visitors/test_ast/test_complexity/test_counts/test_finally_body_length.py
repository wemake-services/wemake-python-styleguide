import pytest

from wemake_python_styleguide.compat.constants import PY311
from wemake_python_styleguide.violations.complexity import (
    TooLongFinallyBodyViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    TryExceptVisitor,
)

try_finally_without_except = """
try:
    ...
finally:
    {0}
"""

simple_try_except_finally = """
try:
    ...
except ValueError:
    ...
finally:
    {0}
"""

try_star_except_finally = """
try:
    ...
except* ValueError:
    ...
finally:
    {0}
"""

full_except_with_else = """
try:
    ...
except ValueError:
    ...
else:
    ...
finally:
    {0}
"""


@pytest.mark.parametrize(
    'statements',
    [
        'print(1)\n    print(2)\n    print(3)',
        'm.print(1)\n    m.print(2)\n    m.print(3)',
        'm = 1\n    p = 2\n    c = 3\n    x = 4',
    ],
)
@pytest.mark.parametrize(
    'code',
    [
        try_finally_without_except,
        simple_try_except_finally,
        full_except_with_else,
        pytest.param(
            try_star_except_finally,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
    ],
)
def test_finally_body_count_default(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    statements,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code.format(statements))

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongFinallyBodyViolation])


@pytest.mark.parametrize(
    'statements',
    [
        'print(1)\n    print(2)\n    print(3)',
        'm.print(1)\n    m.print(2)\n    m.print(3)',
        'm = 1\n    p = 2\n    c = 3',
    ],
)
@pytest.mark.parametrize(
    'code',
    [
        try_finally_without_except,
        simple_try_except_finally,
        full_except_with_else,
        pytest.param(
            try_star_except_finally,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
    ],
)
def test_finally_body_wrong_custom_options(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    options,
    code,
    statements,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code.format(statements))

    option_values = options(max_try_body_length=1)
    visitor = TryExceptVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongFinallyBodyViolation])
    assert_error_text(
        visitor,
        '3',
        baseline=option_values.max_lines_in_finally,
    )


@pytest.mark.parametrize(
    'statements',
    [
        'print(1)\n    print(2)\n    print(3)',
        'm.print(1)\n    m.print(2)\n    m.print(3)',
        'm = 1\n    p = 2\n    c = 3',
    ],
)
@pytest.mark.parametrize(
    'code',
    [
        try_finally_without_except,
        simple_try_except_finally,
        full_except_with_else,
        pytest.param(
            try_star_except_finally,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
    ],
)
def test_finally_body_count_custom_options(
    assert_errors,
    parse_ast_tree,
    options,
    code,
    statements,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code.format(statements))

    option_values = options(max_lines_in_finally=3)
    visitor = TryExceptVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'statements',
    [
        'print(1)',
        'm.print(1)',
        'm = 1',
        'print(\n   1\n)',
        'print(\n   1,\n    2\n)',
        'print(\n   1\n)\nprint(\n   2\n)',
        'print(\n   1,\n    2\n)\nprint(\n   3,\n    4\n)',
    ],
)
@pytest.mark.parametrize(
    'code',
    [
        try_finally_without_except,
        simple_try_except_finally,
        full_except_with_else,
        pytest.param(
            try_star_except_finally,
            marks=pytest.mark.skipif(
                not PY311,
                reason='ExceptionGroup was added in python 3.11',
            ),
        ),
    ],
)
def test_finally_body_correct_default(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    statements,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code.format(statements))

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
