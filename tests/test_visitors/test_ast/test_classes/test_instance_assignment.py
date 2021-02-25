import pytest

from wemake_python_styleguide.violations.best_practices import (
    InstanceLambdaAssignmentViolation,
)
from wemake_python_styleguide.visitors.ast.classes import (
    InstanceAssignmentVisitor,
)

instance_lambda_assignment = """
class Example(object):
    def __init__(self):
        {0}.{1} = lambda: ...
"""


@pytest.mark.parametrize('reference', [
    'self',
    'cls',
    'mcs',
    'other',
])
@pytest.mark.parametrize('attr', [
    'attr',
    '_attr',
    '__attr',
])
def test_instance_lambda_assignment(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    reference,
    attr,
    mode,
):
    """Testing lambda assignment to instance."""
    tree = parse_ast_tree(mode(instance_lambda_assignment.format(
        reference, attr,
    )))

    visitor = InstanceAssignmentVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [InstanceLambdaAssignmentViolation])
