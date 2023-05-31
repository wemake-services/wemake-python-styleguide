import pytest

from wemake_python_styleguide.violations.best_practices import (
    ComplexDefaultValueViolation,
    PositionalOnlyArgumentsViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionSignatureVisitor,
)

function_with_defaults = """
def function(arg, with_default={0}):
    ...
"""

function_with_posonly_defaults = """
def function(with_default={0}, /):
    ...
"""

function_with_kw_defaults1 = """
def function(*, with_default={0}):
    ...
"""

function_with_kw_defaults2 = """
def function(*, arg, with_default={0}):
    ...
"""

method_with_defaults = """
class Test(object):
    def function(self, with_default={0}):
        ...
"""

method_with_posonly_defaults = """
class Test(object):
    def function(self, with_default={0}, /):
        ...
"""

method_with_kw_defaults = """
class Test(object):
    def function(self, *, with_default={0}):
        ...
"""

lambda_with_defaults = 'lambda with_default={0}: ...'
lambda_with_posonly_defaults = 'lambda with_default={0}, /: ...'
lambda_with_kw_defaults = 'lambda *, arg, with_default={0}: ...'

all_templates = (
    function_with_defaults,
    function_with_posonly_defaults,
    function_with_kw_defaults1,
    function_with_kw_defaults2,

    method_with_defaults,
    method_with_posonly_defaults,
    method_with_kw_defaults,

    lambda_with_defaults,
    lambda_with_posonly_defaults,
    lambda_with_kw_defaults,
)


@pytest.mark.parametrize('template', all_templates)
@pytest.mark.parametrize('code', [
    "'PYFLAKES_DOCTEST' in os.environ",
    'call()',
    'call().attr',
    '-call()',
    '+call()',
    'index[1]',
    'index["s"]',
    'index[name][name]',
    'index[1].attr',
    '-index[1].attr',
    'index[1].attr.call().sub',
    'compare == 1',
    'var + 2',
    'a and b',
])
def test_wrong_function_defaults(
    assert_errors,
    parse_ast_tree,
    default_options,
    template,
    code,
    mode,
):
    """Testing that wrong function defaults are forbidden."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [ComplexDefaultValueViolation],
        ignored_types=PositionalOnlyArgumentsViolation,
    )


@pytest.mark.parametrize('template', all_templates)
@pytest.mark.parametrize('code', [
    "'string'",
    "b''",
    '1',
    '-0',
    'variable',
    '-variable',
    'module.attr',
    '-module.attr',
    '(1, 2)',
    '()',
    'None',
    'True',
    'False',
    '...',
])
def test_correct_function_defaults(
    assert_errors,
    parse_ast_tree,
    default_options,
    template,
    code,
    mode,
):
    """Testing that correct function defaults passes validation."""
    tree = parse_ast_tree(mode(template.format(code)))

    visitor = FunctionSignatureVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ignored_types=PositionalOnlyArgumentsViolation)
