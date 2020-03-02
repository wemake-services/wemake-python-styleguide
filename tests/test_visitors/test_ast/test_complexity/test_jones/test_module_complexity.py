import pytest

from wemake_python_styleguide.visitors.ast.complexity.jones import (
    JonesComplexityVisitor,
    JonesScoreViolation,
)

module_without_nodes = ''
module_with_nodes = """
some_value = 1 + 2
other = some_value if some_value > 2 else some_value * 8 + 34
"""

module_with_function = """
def some_function(param):
    return param + param * 2

some_function(12 + 6)
"""

module_with_class = """
class SomeClass(object):
    def execute(self):
        return self

some = SomeClass()
print(some.execute())
"""


@pytest.mark.parametrize('code', [
    module_without_nodes,
    module_with_nodes,
    module_with_function,
    module_with_class,
])
def test_module_score(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that regular nodes do not raise violations."""
    tree = parse_ast_tree(mode(code))

    visitor = JonesComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('code', 'score'), [
    (module_without_nodes, 0),
    (module_with_nodes, 8.5),
    (module_with_function, 6),
    (module_with_class, 2),
])
def test_module_score_error(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    score,
    options,
    mode,
):
    """Testing that regular nodes do raise violations."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_jones_score=-1)
    visitor = JonesComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [JonesScoreViolation])
    assert_error_text(visitor, str(score), option_values.max_jones_score)
