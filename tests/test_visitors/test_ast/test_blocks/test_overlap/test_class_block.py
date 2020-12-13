import pytest

from wemake_python_styleguide.violations.best_practices import (
    BlockAndLocalOverlapViolation,
)
from wemake_python_styleguide.visitors.ast.blocks import BlockVariableVisitor

# Classes:

class_def1 = 'class {0}():'
class_def2 = 'class {0}(object):'
class_def3 = 'class {0}:'

# Wrong usages:

class_template1 = """
{0}
    ...

{1}
"""

class_template2 = """
{0}
    {1}

    def {2}(self): ...
"""


@pytest.mark.parametrize('class_statement', [
    class_def1,
    class_def2,
    class_def3,
])
@pytest.mark.parametrize('context', [
    class_template1,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_class_block_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    class_statement,
    assign_and_annotation_statement,
    context,
    variable_name,
    default_options,
):
    """Ensures that overlapping variables exist."""
    code = context.format(
        class_statement.format(variable_name),
        assign_and_annotation_statement.format(variable_name),
    )
    tree = parse_ast_tree(code)

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, variable_name)


@pytest.mark.parametrize('class_statement', [
    class_def1,
    class_def2,
    class_def3,
])
@pytest.mark.parametrize('context', [
    class_template2,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_class_internals_overlap(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    class_statement,
    assign_statement,
    context,
    variable_name,
    default_options,
):
    """Ensures that overlapping variables exist."""
    code = context.format(
        class_statement.format('UniqueClassName'),
        assign_statement.format(variable_name),
        variable_name,
    )
    tree = parse_ast_tree(code)

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BlockAndLocalOverlapViolation])
    assert_error_text(visitor, variable_name)


@pytest.mark.parametrize('class_statement', [
    class_def1,
    class_def2,
    class_def3,
])
@pytest.mark.parametrize('context', [
    class_template1,
])
@pytest.mark.parametrize('variable_name', [
    'should_raise',
])
def test_class_block_usage(
    assert_errors,
    parse_ast_tree,
    class_statement,
    context,
    variable_name,
    default_options,
):
    """Ensures using variables is fine."""
    code = context.format(
        class_statement.format(variable_name),
        'print({0})'.format(variable_name),
    )
    tree = parse_ast_tree(code)

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('class_statement', [
    class_def1,
    class_def2,
    class_def3,
])
@pytest.mark.parametrize('context', [
    class_template1,
])
@pytest.mark.parametrize(('first_name', 'second_name'), [
    ('unique_name', 'unique_name1'),
    ('_', '_'),
])
def test_class_block_correct(
    assert_errors,
    parse_ast_tree,
    class_statement,
    assign_and_annotation_statement,
    context,
    first_name,
    second_name,
    default_options,
):
    """Ensures that different variables do not overlap."""
    code = context.format(
        class_statement.format(first_name),
        assign_and_annotation_statement.format(second_name),
    )
    tree = parse_ast_tree(code)

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('class_statement', [
    class_def1,
    class_def2,
    class_def3,
])
@pytest.mark.parametrize('context', [
    class_template2,
])
@pytest.mark.parametrize(('first_name', 'second_name'), [
    ('unique_name', 'unique_name1'),
    ('_', '_'),
])
def test_class_internal_block_correct(
    assert_errors,
    parse_ast_tree,
    class_statement,
    assign_and_annotation_statement,
    context,
    first_name,
    second_name,
    default_options,
):
    """Ensures that different variables do not overlap."""
    code = context.format(
        class_statement.format('SomeUniqueClassName'),
        assign_and_annotation_statement.format(second_name),
        first_name,
    )
    tree = parse_ast_tree(code)

    visitor = BlockVariableVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
