import pytest

from wemake_python_styleguide.violations.best_practices import FloatKeyViolation
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongCollectionVisitor,
)

dict_template1 = '{{ {0}: 1 }}'
dict_template2 = '{{ {0}: {0} }}'
dict_template3 = '{{ {0}: 1, **kwargs }}'
dict_template4 = '{{ {0}: 1, other: value }}'


@pytest.mark.parametrize('code', [
    dict_template1,
    dict_template2,
    dict_template3,
    dict_template4,
])
@pytest.mark.parametrize('element', [
    '1.0',
    '-0.3',
    '+0.0',
    '1 / 3',
    '-1 - 0.5',
    '0 + 0.1',
])
def test_dict_with_float_key(
    assert_errors,
    parse_ast_tree,
    code,
    element,
    default_options,
):
    """Testing that float keys are not allowed."""
    tree = parse_ast_tree(code.format(element, element))

    visitor = WrongCollectionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FloatKeyViolation])


@pytest.mark.parametrize('code', [
    dict_template1,
    dict_template2,
    dict_template3,
    dict_template4,
])
@pytest.mark.parametrize('element', [
    '1',
    '"-0.3"',
    '1 // 3',
    'call()',
    'name',
    'attr.some',
    'done[key]',
])
def test_dict_with_regular(
    assert_errors,
    parse_ast_tree,
    code,
    element,
    default_options,
):
    """Testing that regular keys are allowed."""
    tree = parse_ast_tree(code.format(element, element))

    visitor = WrongCollectionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
