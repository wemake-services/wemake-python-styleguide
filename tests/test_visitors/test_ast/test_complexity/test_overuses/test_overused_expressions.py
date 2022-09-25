import pytest

from wemake_python_styleguide.violations.complexity import (
    OverusedExpressionViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.overuses import (
    ExpressionOveruseVisitor,
)

module_context = """
{0}
{1}
"""

function_context1 = """
def function():
    {0}
    {1}
"""

function_context2 = """
@decorator
def function() -> types.Some[None]:
    {0}
    {1}
"""

function_context3 = """
@decorator()
def function(arg: List[int]) -> types.NoneType[None]:
    {0}
    {1}
"""

function_context4 = """
@decorator.attr.nested()
def function(arg: List[int]) -> types.NoneType[None]:
    {0}
    {1}
"""

class_context1 = """
class Context(object):
    {0}
    {1}
"""

class_context2 = """
class Context(object):
    first: List[int]
    second: List[int]

    {0}
    {1}
"""

class_context3 = """
class Context(object):
    first: List[List[int]]
    second: List[List[int]]

    {0}
    {1}
"""

method_context1 = """
class Context(object):
    def method(self):
        {0}
        {1}
"""

method_context2 = """
class Context(object):
    @decorator.attr
    @decorator.attr
    def method(self):
        {0}
        {1}
"""

method_context3 = """
class Context(object):
    @decorator.call('a')
    @decorator.call('a')
    def method(self, arg: List[int]) -> type.Any:
        {0}
        {1}
"""

# regression for:
# https://github.com/wemake-services/wemake-python-styleguide/issues/1152
method_context4 = """
class Context(object):
    def method1(self, arg1: List[int]) -> type.Any:
        {0}
        {0}

    # Two methods have the same signature, that's how we check
    # for return and arg annotations.
    def method2(self, arg2: List[int]) -> type.Any:
        ...
"""

method_context5 = """
class Context(object):
    def method1(self, arg1: "List[int]") -> 'type.Any':
        ...

    # Two methods have the same signature, that's how we check
    # for return and arg annotations.
    def method2(self, arg2: "List[int]") -> 'type.Any':
        {0}
        {0}
"""

# Expressions:

violating_expressions = (
    # Nodes:
    'assert 1',  # statement, but still
    'a and b',
    'b + a',
    'call(1, None)',
    'a >= 1',
    'lambda x: x.set',
    '{a: 1 for a in "123"}',
    '{"1": a}',
    '[element, other]',
    '[x for x in some if cond]',
    '(1, 2, 3)',
    '(x.attr for x in other)',
    '{1, 2, 3}',
    '{a for a in other}',

    # Unary nodes:
    '+some',  # unary plus always raises
    '~other',

    # Special cases for self:
    'self.method([star])',  # `[star]` is raising
    'self[1, 2, 3]',  # tuple is raising

    # Annotations:
    'x: types.List[Set[int]] = call(1, 2, 3)',  # call is raising
)

ignored_expressions = (
    # super
    'super()',
    # special attrs
    'self.call(1, 2, 3)',
    'cls.__private_attribute()',
    'mcs._property()',
    'self[start:end]',
    # primitives
    '[]',
    '()',
    '{**keys}',
    '{*set_items}',  # there's no empty set literal
    '""',
    '1',
    'b"context"',
    # simplest calls, regression1152
    'list()',
    'set()',
    'dict()',
    # attributes
    'some.prop',
    # unary operator
    '-value',
    '-value.attr',
    '-1',
)


@pytest.mark.parametrize('code', [
    function_context1,
    function_context2,
    function_context3,
    function_context4,
    method_context1,
    method_context2,
    method_context3,
    method_context4,
    method_context5,
])
@pytest.mark.parametrize('expression', violating_expressions)
def test_func_expression_overuse(
    assert_errors,
    parse_ast_tree,
    options,
    expression,
    code,
    mode,
):
    """Ensures that settings for expressions over-use work."""
    tree = parse_ast_tree(mode(code.format(expression, expression)))

    option_values = options(max_function_expressions=1)
    visitor = ExpressionOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [OverusedExpressionViolation])


@pytest.mark.parametrize('code', [
    module_context,
])
@pytest.mark.parametrize('expression', violating_expressions)
def test_module_expression_overuse(
    assert_errors,
    parse_ast_tree,
    options,
    expression,
    code,
):
    """Ensures that settings for expressions over-use work."""
    tree = parse_ast_tree(code.format(expression, expression))

    option_values = options(max_module_expressions=1)
    visitor = ExpressionOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [OverusedExpressionViolation])


@pytest.mark.parametrize('code', [
    class_context1,
    class_context2,
    class_context3,
])
@pytest.mark.parametrize('expression', violating_expressions)
def test_class_expression_use(
    assert_errors,
    parse_ast_tree,
    options,
    expression,
    code,
):
    """Ensures that settings for expressions over-use work."""
    tree = parse_ast_tree(code.format(expression, expression))

    option_values = options(
        max_module_expressions=1,
        max_function_expressions=1,
    )
    visitor = ExpressionOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    function_context1,
    function_context2,
    function_context3,
    function_context4,
    class_context1,
    class_context2,
    class_context3,
    method_context1,
    method_context2,
    method_context3,
    method_context4,
    method_context5,
    module_context,
])
@pytest.mark.parametrize('expression', ignored_expressions)
def test_ignored_expressions(
    assert_errors,
    parse_ast_tree,
    options,
    expression,
    code,
    mode,
):
    """Ensures that ignored expressions does not raise violations."""
    tree = parse_ast_tree(mode(code.format(expression, expression)))

    option_values = options(max_function_expressions=1)
    visitor = ExpressionOveruseVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
