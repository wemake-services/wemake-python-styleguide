from typing import Iterable

from wemake_python_styleguide.compat.nodes import Match, MatchAs, match_case
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.walk import get_subnodes_by_type


def get_explicit_as_names(
    node: Match,
) -> Iterable[MatchAs]:  # pragma: py-lt-310
    """
    Returns variable names defined as ``case ... as var_name``.

    Does not return variables defined as ``case var_name``.
    Or in any other forms.
    """
    for match_as in get_subnodes_by_type(node, MatchAs):
        if isinstance(get_parent(match_as), match_case):
            if match_as.pattern and match_as.name:
                yield match_as
