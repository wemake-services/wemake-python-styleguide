import pytest

from wemake_python_styleguide.violations.consistency import (
    ConsecutiveSlicesViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import (
    ConsecutiveSlicesVisitor,
)

template = 'a[{0}][{1}][{2}][{3}][{4}]'


@pytest.mark.parametrize('slice_statement', [
    template,
])
@pytest.mark.parametrize('seeds', [
    ['1:', '2:', '3', '4', '5'],
    ['1:', '2:', '3:', '4', '5'],
    ['1:', '2:', '3:', '4:', '5'],
    ['1:', '2:', '3:', '4:', '5:'],
    ['1', '2:', '3:', '4', '5'],
    ['1', '2', ':3', '4:', '5'],
    ['1', '2', ':3', '4:', '5:'],
])
def test_slicing(
    assert_errors, parse_ast_tree, slice_statement, seeds, default_options,
):
    """Testing cases that raise the violation."""
    code = slice_statement.format(*seeds)
    tree = parse_ast_tree(code)
    visitor = ConsecutiveSlicesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConsecutiveSlicesViolation])


@pytest.mark.parametrize('slice_statement', [
    template,
])
@pytest.mark.parametrize('seeds', [
    ['1', '2:', '3', '4', '5'],
    ['1', '2', '3:', '4', '5'],
    ['1', '2', '3', '4:', '5'],
    ['1', '2', '3', '4', '5:'],
    ['1', '2:', '3', '4:', '5'],
    ['1', '2', ':3', '4', '5:'],
])
def test_no_slicing(
    assert_errors, parse_ast_tree, slice_statement, seeds, default_options,
):
    """Testing cases that does not raise the violation."""
    code = slice_statement.format(*seeds)
    tree = parse_ast_tree(code)
    visitor = ConsecutiveSlicesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('slice_statement', [
    template,
])
@pytest.mark.parametrize('seeds', [
    ['1:', '2:', '3', '4:', ':5'],
])
def test_double_slicing(
    assert_errors, parse_ast_tree, slice_statement, seeds, default_options,
):
    """Testing cases that raise the violation."""
    code = slice_statement.format(*seeds)
    tree = parse_ast_tree(code)
    violations = [ConsecutiveSlicesViolation, ConsecutiveSlicesViolation]
    visitor = ConsecutiveSlicesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, violations)
