import pytest

from wemake_python_styleguide.violations.best_practices import (
    NonUniqueItemsInHashViolation,
    UnhashableTypeInHashViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongCollectionVisitor,
)

set_literal_template = '{{{0}, {1}}}'
nested_set_template = """
{{
    *{{
        {0},
        {1},
    }},
}}
"""

dict_literal_template = '{{ {0}: 1, {1}: 2 }}'


@pytest.mark.parametrize('code', [
    set_literal_template,
    nested_set_template,
    dict_literal_template,
])
@pytest.mark.parametrize('element', [
    '[item.call()]',
    '{"key": some_value.attr}',
    '{some_value.attr, some_other}',
    "{'key': value}",
    "{'', '1', True}",
    '[]',
    '[name, name2]',
    '(x for x in some())',
    '[x for x in some()]',
    '{x for x in some()}',
    '{x: 1 for x in some()}',
])
def test_hash_with_impure(
    assert_errors,
    parse_ast_tree,
    code,
    element,
    default_options,
):
    """Testing that impure elements can be contained in hash."""
    tree = parse_ast_tree(code.format(element, 'correct'))

    visitor = WrongCollectionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnhashableTypeInHashViolation])


@pytest.mark.parametrize('code', [
    set_literal_template,
    nested_set_template,
    dict_literal_template,
])
@pytest.mark.parametrize('element', [
    '{"key": some_value}',
    "{value: 'key'}",
    "{'', '1', True}",
    '[]',
    '[name, name2]',
    '{1, 2}',
    '{True, False, None}',
])
def test_hash_with_impure_duplicates(
    assert_errors,
    parse_ast_tree,
    code,
    element,
    default_options,
):
    """Testing that impure elements can be contained in hash."""
    tree = parse_ast_tree(code.format(element, element))

    visitor = WrongCollectionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        NonUniqueItemsInHashViolation,
        UnhashableTypeInHashViolation,
        UnhashableTypeInHashViolation,
    ])
