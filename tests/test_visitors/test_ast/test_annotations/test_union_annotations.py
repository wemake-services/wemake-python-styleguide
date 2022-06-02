import pytest

from wemake_python_styleguide.violations.best_practices import (
    DisallowUnionTypeViolation,
)
from wemake_python_styleguide.visitors.ast.annotations import (
    WrongAnnotationVisitor,
)


@pytest.mark.parametrize(
    'function',
    [
        """def function(a: Union[int, str]): ...""",
        """def function(a: typing.Union[int, str]): ...""",
        """def function(a: t.Union[int, str]): ...""",
        """def function(a: List[Union[int, str]]): ...""",
        """def function(a: int) -> Union[int, str]: ...""",
        """def function(a: Optional[int]) -> None: ...""",
    ],
)
def test_wrong_return_annotation(
    assert_errors,
    parse_ast_tree,
    function,
    default_options,
    mode,
) -> None:
    """Ensures that using incorrect return annotations is forbidden."""
    tree = parse_ast_tree(mode(function))

    visitor = WrongAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [DisallowUnionTypeViolation])
