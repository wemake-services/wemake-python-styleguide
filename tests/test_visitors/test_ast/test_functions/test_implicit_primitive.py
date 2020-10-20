import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitPrimitiveViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    UselessLambdaDefinitionVisitor,
)


@pytest.mark.parametrize('code', [
    'lambda x: 0',
    'lambda *x: []',
    'lambda **x: ()',
    'lambda x, y: 0',
    'lambda: 1',
    'lambda x=1: 0',
    'lambda: [0]',
    'lambda: [some]',
    'lambda: None',
    'lambda: True',
    'lambda: "a"',
    'lambda: b"a"',
    'lambda: (1, 2)',
    'lambda: name',
])
def test_correct_lambda(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that isinstance is callable with correct types."""
    tree = parse_ast_tree(code)

    visitor = UselessLambdaDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'lambda: 0',
    'lambda: 0.0',
    'lambda: 0j',
    'lambda: b""',
    'lambda: ""',
    'lambda: []',
    'lambda: ()',
    'lambda: False',
    'lambda: lambda: ""',
    'lambda: {}',  # noqa: P103
])
def test_wrong_lambda(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that isinstance is callable with correct types."""
    tree = parse_ast_tree(code)

    visitor = UselessLambdaDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitPrimitiveViolation])
