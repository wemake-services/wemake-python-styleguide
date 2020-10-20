import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyBaseClassesViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.classes import (
    ClassComplexityVisitor,
)

correct_count = """
class CorrectClassName(
    FirstParentClass,
    SecondParentClass,
    ThirdParentClass,
): ...
"""

correct_count_with_keywords = """
class CorrectClassName(
    FirstParentClass,
    SecondParentClass,
    ThirdParentClass,
    first=1,
    second=2,
    third=3,
    fourth=4,
    fifth=5,
): ...
"""

too_many_count = """
class SomeClassName(
    FirstParentClass,
    SecondParentClass,
    ThirdParentClass,
    CustomClass,
    AddedClass,
): ...
"""


@pytest.mark.parametrize('code', [
    correct_count,
    correct_count_with_keywords,
])
def test_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing of correct base classes number."""
    tree = parse_ast_tree(code)

    visitor = ClassComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    too_many_count,
])
def test_bad_number_default_option(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing of base classes number with default options."""
    tree = parse_ast_tree(code)

    visitor = ClassComplexityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyBaseClassesViolation])
    assert_error_text(visitor, '5', default_options.max_base_classes)


@pytest.mark.parametrize('code', [
    too_many_count,
    correct_count,
    correct_count_with_keywords,
])
def test_bad_number_custom_option(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing of base classes number with custom options."""
    tree = parse_ast_tree(code)

    options = options(max_base_classes=5)
    visitor = ClassComplexityVisitor(options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
