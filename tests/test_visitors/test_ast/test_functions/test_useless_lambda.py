import pytest

from wemake_python_styleguide.violations.refactoring import (
    UselessLambdaViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    UselessLambdaDefinitionVisitor,
)

template = '{0}: {1}'

useless_lambdas = [
    ('lambda', 'method()'),
    ('lambda x', 'method(x)'),
    ('lambda x, y', 'method(x, y)'),
    ('lambda *, x, y', 'method(x=x, y=y)'),  # order 1
    ('lambda *, x, y', 'method(y=y, x=x)'),  # order 2
    ('lambda x, *, y', 'method(x, y=y)'),
    ('lambda x, *y', 'method(x, *y)'),
    ('lambda x, **z', 'method(x, **z)'),
    ('lambda x, *y, **z', 'method(x, *y, **z)'),
    ('lambda *args, **kwargs', 'method(*args, **kwargs)'),

    # with `/`:
    ('lambda x, /, y', 'method(x, y)'),
    ('lambda x, /, y, *, z', 'method(x, y, z=z)'),
    ('lambda x, /, y, *arg, z, **kw', 'method(x, y, *arg, z=z, **kw)'),
]


@pytest.mark.parametrize(('lambda_def', 'call_def'), useless_lambdas)
def test_incorrect_lambda_definition(
    assert_errors,
    parse_ast_tree,
    lambda_def,
    call_def,
    default_options,
):
    """Testing useless lambdas are reported."""
    tree = parse_ast_tree(template.format(lambda_def, call_def))

    visitor = UselessLambdaDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UselessLambdaViolation])


valid_calls = (
    '[1, 2, 3]',
    'method',
    'obj.attr',
    'obj.call()',
    'obj.call(x)',
    'method(argument_with_different_name)',
    'method(1)',
    'method(x=9)',
    'method(y, x)',
    'method(x.attr, y.attr)',
    'method(x=x)',
    'method(x=x.attr, y=y.attr)',
    'method(x=y, y=x)',
    'method(y=x, x=y)',
    'method(x=x, y=1)',
    'method(x=x, y=y, z=z)',
    'method(x=x, y=y, *args)',
    'method(x=x, y=y, **kwargs)',
    'method(x=x, y=y, z=1)',
    'method(a, x=x, y=y)',
    'method(x, *z)',
    'method(*y)',
    'method(x, **y)',
    'method(**z)',
    'method(*args)',
    'method(**kwargs)',
    'method(x, *args, **kwargs)',
    'method(*args, **kwargs)',
    'method(*())',
    'method(**{{}})',
    'method(x, *[], **{{}})',
)


@pytest.mark.parametrize('lambda_def', [
    'lambda x',
    'lambda x=1',
    'lambda *, x=1',
    'lambda x, y',
    'lambda x, *, y',
    'lambda y, *, x',
    'lambda *, x, y',
    'lambda *, y, x',
    'lambda x, *y',
    'lambda x, **z',
    'lambda x, *y, **z',
    'lambda *y, **z',
    'lambda *only_y',
    'lambda **only_z',
])
@pytest.mark.parametrize('inner_def', [
    *valid_calls,
    'method()',
])
def test_correct_lambda_definition(
    assert_errors,
    parse_ast_tree,
    lambda_def,
    inner_def,
    default_options,
):
    """Testing correct lambdas are not reported."""
    tree = parse_ast_tree(template.format(lambda_def, inner_def))

    visitor = UselessLambdaDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('inner_def', valid_calls)
def test_correct_empty_lambda_definition(
    assert_errors,
    parse_ast_tree,
    inner_def,
    default_options,
):
    """Testing correct empty lambdas are not reported."""
    tree = parse_ast_tree(template.format('lambda', inner_def))

    visitor = UselessLambdaDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
