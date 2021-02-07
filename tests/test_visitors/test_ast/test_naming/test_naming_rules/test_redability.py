import pytest

from wemake_python_styleguide import constants
from wemake_python_styleguide.logic.naming.alphabet import (
    get_unreadable_characters,
)
from wemake_python_styleguide.violations.naming import (
    UnreadableNameViolation,
    UpperCaseAttributeViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)


@pytest.mark.parametrize('expression', [
    'My1Item',
    'Element0Operation',
    'O0S',
    'S0O',
])
def test_unreadable_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    own_naming_template,
    expression,
    default_options,
    mode,
):
    """Ensures that unreadable names are not allowed."""
    tree = parse_ast_tree(
        mode(own_naming_template.format(expression, expression)),
    )

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    unreadable = get_unreadable_characters(
        expression, constants.UNREADABLE_CHARACTER_COMBINATIONS,
    )

    assert_errors(
        visitor,
        [UnreadableNameViolation],
        ignored_types=UpperCaseAttributeViolation,
    )
    assert_error_text(
        visitor,
        unreadable,
        ignored_types=UpperCaseAttributeViolation,
    )
