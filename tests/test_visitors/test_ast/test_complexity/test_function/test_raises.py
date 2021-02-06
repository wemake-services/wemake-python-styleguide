import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyRaisesViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
)

module_many_raises = """
if some:
    raise SomeException
raise SomeOtherException
"""

lambda_many_raises = """
lambda: SomeException if some else SomeOtherException
"""

function_template = """
def function(parameter):
    {0}
    {1}
    {2}
"""

instance_method_template = """
class Test(object):
    def method(self, parameter):
        {0}
        {1}
        {2}
"""

class_method_template = """
class Test(object):
    @classmethod
    def method(cls, parameter):
        {0}
        {1}
        {2}
"""

static_method_template = """
class Test(object):
    @staticmethod
    def method(parameter):
        {0}
        {1}
        {2}
"""


@pytest.mark.parametrize('code', [
    module_many_raises,
    lambda_many_raises,
])
def test_asserts_correct_count1(
    assert_errors,
    parse_ast_tree,
    options,
    code,
):
    """Testing that raises counted correctly."""
    tree = parse_ast_tree(code)

    option_values = options(max_raises=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('context', [
    function_template,
    instance_method_template,
    class_method_template,
    static_method_template,
])
@pytest.mark.parametrize(('first', 'second', 'third'), [
    ('...', '', ''),
    ('if some:', '    raise SomeException', 'raise SomeOtherException'),
    ('def helper():', '    raise SomeException', 'raise SomeOtherException'),
])
def test_raises_correct_count2(
    assert_errors,
    parse_ast_tree,
    context,
    first,
    second,
    third,
    default_options,
    mode,
):
    """Testing that raises are counted correctly."""
    test_instance = context.format(first, second, third)
    tree = parse_ast_tree(mode(test_instance))

    visitor = FunctionComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('context', [
    function_template,
    instance_method_template,
    class_method_template,
    static_method_template,
])
@pytest.mark.parametrize(('first', 'second', 'third'), [
    ('if some:', '    raise SomeException', 'raise SomeOtherException'),
    ('def helper():', '    raise SomeException', 'raise SomeOtherException'),
])
def test_raises_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    options,
    context,
    first,
    second,
    third,
    mode,
):
    """Testing that many raises raises a warning."""
    test_instance = function_template.format(first, second, third)
    tree = parse_ast_tree(mode(test_instance))

    option_values = options(max_raises=1)
    visitor = FunctionComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyRaisesViolation])
    assert_error_text(visitor, '2', option_values.max_raises)
