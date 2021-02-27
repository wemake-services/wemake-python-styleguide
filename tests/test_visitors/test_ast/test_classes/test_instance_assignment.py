import pytest

from wemake_python_styleguide.violations.best_practices import (
    InstanceLambdaAssignmentViolation,
)
from wemake_python_styleguide.visitors.ast.classes import (
    AttributesAssignmentVisitor,
)

instance_lambda_assignment = """
class Example(object):
    def __init__(self):
        {0}
"""

class_lambda_assignment = """
class Example(object):
    {0}
"""


@pytest.mark.parametrize('assignment', [
    'self.attr = lambda: ...',
    'self.attr1 = self.attr2 = lambda: ...',
    'self.attr1, self.attr2 = lambda: ..., "value"',
    'self.attr: Callable[[], None] = lambda: ...',
])
def test_instance_lambda_assignment(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    assignment,
    mode,
):
    """Testing lambda assignment to instance."""
    tree = parse_ast_tree(mode(instance_lambda_assignment.format(assignment)))

    visitor = AttributesAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InstanceLambdaAssignmentViolation])


@pytest.mark.parametrize('assignment', [
    'attr = lambda: ...',
    'attr1 = attr2 = lambda: ...',
    'attr1, attr2 = lambda: ..., "value"',
    'attr: Callable[[], None] = lambda: ...',
])
def test_class_lambda_assignment(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    assignment,
    mode,
):
    """Testing lambda assignment to class."""
    tree = parse_ast_tree(mode(class_lambda_assignment.format(assignment)))

    visitor = AttributesAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InstanceLambdaAssignmentViolation])
