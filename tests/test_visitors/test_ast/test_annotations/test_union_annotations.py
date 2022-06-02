import sys

import pytest

from wemake_python_styleguide.violations.best_practices import (
    DisallowUnionTypeViolation,
)
from wemake_python_styleguide.visitors.ast.annotations import (
    WrongAnnotationVisitor,
)


@pytest.mark.parametrize(
    'expression',
    [
        'def function(a: Union[int, str]): ...',
        'def function(a: typing.Union[int, str]): ...',
        'def function(a: t.Union[int, str]): ...',
        'def function(a: List[Union[int, str]]): ...',
        'def function(a: int) -> Union[int, str]: ...',
        'def function(a: Optional[int]) -> None: ...',
        'a = Union[int, str]',
        'a: Optional[str] = None',
        'a: Optional[Union[int, str]]',
    ],
)
def test_wrong_union_func_annotation(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
    mode,
) -> None:
    """Ensures that using incorrect union annotations is forbidden."""
    tree = parse_ast_tree(mode(expression))

    visitor = WrongAnnotationVisitor(default_options, tree=tree)
    visitor.run()

    if sys.version_info < (3, 10):  # pragma: py-lt-310
        assert_errors(visitor, [])
    else:  # pragma: py-gte-310
        assert_errors(visitor, [DisallowUnionTypeViolation])
