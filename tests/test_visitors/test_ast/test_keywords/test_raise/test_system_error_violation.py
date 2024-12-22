import pytest

from wemake_python_styleguide.violations.consistency import (
    RaiseSystemErrorViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongRaiseVisitor

template = 'raise {0}'


@pytest.mark.parametrize(
    'code',
    [
        'SystemError',
        'SystemError()',
        'SystemError(0)',
        'SystemError(code)',
    ],
)
def test_raise_system_error(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing `raise SystemError` is restricted."""
    tree = parse_ast_tree(template.format(code))

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RaiseSystemErrorViolation])


@pytest.mark.parametrize(
    'code',
    [
        'NotImplementedError',
        'NotImplementedError()',
        'CustomSystemError',
        'CustomSystemError()',
        'custom.SystemError',
        'custom.SystemError()',
    ],
)
def test_raise_good_errors(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that other exceptions are allowed."""
    tree = parse_ast_tree(template.format(code))

    visitor = WrongRaiseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
