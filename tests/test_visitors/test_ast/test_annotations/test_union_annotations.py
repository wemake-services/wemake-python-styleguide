import pytest

from wemake_python_styleguide.violations.best_practices import (
    DisallowUnionTypeViolation,
)
from wemake_python_styleguide.visitors.ast.annotations import (
    WrongAnnotationVisitor,
)

functions_breaking_rule = [
    """def function(a: Union[int, str]): ...""",
    """def function(a: typing.Union[int, str]): ...""",
    """def function(a: t.Union[int, str]): ...""",
    """def function(a: List[Union[int, str]]): ...""",
    """def function(a: int) -> Union[int, str]: ...""",
    """def function(a: Optional[int]) -> None: ...""",
]


@pytest.mark.parametrize('function', functions_breaking_rule)
def test_wrong_return_annotation(
    assert_errors,
    parse_ast_tree,
    function,
    options,
    mode,
) -> None:
    """Ensures that using incorrect return annotations is forbidden."""
    tree = parse_ast_tree(mode(function))

    visitor = WrongAnnotationVisitor(
        options(disallow_union_type=True),
        tree=tree,
    )
    visitor.run()

    assert_errors(visitor, [DisallowUnionTypeViolation])
