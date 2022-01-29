import pytest

from wemake_python_styleguide.logic.complexity import annotations


@pytest.mark.parametrize(('annotation', 'complexity'), [
    # simple annotations
    ('str', 1),
    ('int', 1),
    ('List', 1),
    ('List[str]', 2),
    ('List[int]', 2),
    ('Dict[str, int]', 2),

    # empty values
    ('Literal[""]', 2),
    ('Tuple[()]', 2),

    # Literals with strings:
    ('Literal["regular", "raise", "is"]', 2),

    # invalid annotations
    ('"This is rainbow in the dark!"', 1),

    # complex annotations
    ('Tuple[List[int], Optional[Dict[str, int]]]', 4),
])
def test_get_annotation_complexity(
    parse_ast_tree, annotation: str, complexity: int,
) -> None:
    """Test get_annotation_complexity function."""
    text = 'def f() -> {annotation}: pass\n'.format(annotation=annotation)
    tree = parse_ast_tree(text)
    node = tree.body[0].returns
    assert annotations.get_annotation_complexity(node) == complexity
