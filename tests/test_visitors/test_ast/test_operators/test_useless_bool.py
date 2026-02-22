import pytest

from wemake_python_styleguide.violations.consistency import (
    MeaninglessBooleanOperationViolation,
)
from wemake_python_styleguide.visitors.ast.operators import (
    UselessOperatorsVisitor,
)


@pytest.mark.parametrize(
    'expression',
    [
        # containing constants only
        '2 and -2',
        'True and 0 and "py"',
        'False or 2 or "py"',
        # `and` containing at least one constant
        'value and True',
        'value1 and 4 and value2 and "py" and True',
        # `or` containing True/False
        'value or False',
        'value1 or True or value2 or False or False',
        # `or` containing everything after non-bool constant
        'value1 or 0 or value2',
        'value or "py" or 4',
        # `and`/`or` operators containing a duplicate name
        # with identical unary operations
        'value and value and value',
        'value or value or value',
        'value1 and value2 and value1',
        'value2 or value1 or value1',
        'value or --value',
        '~value or value or ~value',
        # complex expression containing one of the cases listed above
        '(value1 and value2) or (1 and 2)',
    ],
)
def test_useless_bool(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that some bool operations are useless."""
    tree = parse_ast_tree(expression)

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MeaninglessBooleanOperationViolation])


@pytest.mark.parametrize(
    'expression',
    [
        'value or -value or ~value',
        'value1 or value2 or value3',
        'value1 or value2 or 4',
        'value1 and value2 and value3',
        '(value1 and value2) or (value3 and value4)',
    ],
)
def test_useful_bool(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing that all bool operations are useful."""
    tree = parse_ast_tree(expression)

    visitor = UselessOperatorsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
