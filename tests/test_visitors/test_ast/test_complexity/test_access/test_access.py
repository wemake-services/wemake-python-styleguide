import pytest

from wemake_python_styleguide.violations.complexity import (
    TooDeepAccessViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.access import (
    AccessVisitor,
)

# boundary expressions
subscript_access = 'my_matrix[0][0][0][0]'
attribute_access = 'self.attr.inner.wrapper.value'
mixed_access = 'self.attr[0].wrapper[0]'
mixed_with_calls_access = 'self.attr[0]().wrapper[0][0].bar().foo[0]()'

# correct expressions
call_chain = 'manager.filter().exclude().annotate().values().first()'

# incorrect expressions
deep_access = 'self.some.other.attr().first.second.third.fourth.boom'


@pytest.mark.parametrize('code', [
    subscript_access,
    attribute_access,
    mixed_access,
    mixed_with_calls_access,
    call_chain,
])
def test_correct_access(
    assert_errors,
    parse_ast_tree,
    code,
    options,
    mode,
):
    """Testing that expressions with correct access level work well."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_access_level=4)
    visitor = AccessVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('code', 'access_level'), [
    (subscript_access, 4),
    (attribute_access, 4),
    (mixed_access, 4),
    (mixed_with_calls_access, 4),
    (deep_access, 5),
])
def test_incorrect_access(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    access_level,
    options,
    mode,
):
    """Testing that violations are raised when reaching too deep access."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_access_level=3)
    visitor = AccessVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooDeepAccessViolation])
    assert_error_text(
        visitor,
        access_level,
        option_values.max_access_level,
    )
