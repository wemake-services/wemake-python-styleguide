import pytest

from wemake_python_styleguide.violations.best_practices import (
    MutableModuleConstantViolation,
)
from wemake_python_styleguide.visitors.ast.modules import ModuleConstantsVisitor

module_constant = 'CONST = {0}'
module_typed_constant = 'CONST: int = {0}'

module_variable = 'some_variable = {0}'
module_attribute = 'some.attr = {0}'
module_slice = 'some[0] = {0}'


@pytest.mark.parametrize('assignment', [
    module_constant,
    module_typed_constant,
])
@pytest.mark.parametrize('code', [
    '{1, 2, 3}',
    '[]',
    '{"1": 1}',
    '{tokenize.NL, tokenize.NEWLINE, *MATCHING.values()}',
    '[x for x in "123"]',
    '{x: x for x in "123"}',
    '{x for x in "123"}',
])
def test_wrong_constant_type_used(
    assert_errors,
    parse_ast_tree,
    default_options,
    assignment,
    code,
):
    """Testing that some constants are restricted."""
    tree = parse_ast_tree(assignment.format(code))

    visitor = ModuleConstantsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MutableModuleConstantViolation])


@pytest.mark.parametrize('assignment', [
    module_variable,
    module_attribute,
    module_slice,
])
@pytest.mark.parametrize('code', [
    '{1, 2, 3}',
    '[]',
    '{"1": 1}',
    '[x for x in "123"]',
    '{x: x for x in "123"}',
    '{x for x in "123"}',
])
def test_correct_non_constant(
    assert_errors,
    parse_ast_tree,
    default_options,
    assignment,
    code,
):
    """Testing that some constants are restricted."""
    tree = parse_ast_tree(assignment.format(code))

    visitor = ModuleConstantsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('assignment', [
    module_constant,
    module_typed_constant,
    module_variable,
    module_attribute,
    module_slice,
])
@pytest.mark.parametrize('code', [
    'frozenset((1, 2, 3))',
    '(1, 2)',
    '(1, 2,)',
    'call()',
    '1',
    '"string"',
    'obj.attr',
    'dict[0]',
])
def test_correct_constant_type_used(
    assert_errors,
    parse_ast_tree,
    default_options,
    assignment,
    code,
):
    """Testing that some constants are ok."""
    tree = parse_ast_tree(assignment.format(code))

    visitor = ModuleConstantsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
