from collections import defaultdict
from typing import TypeAlias, final

import attr

from wemake_python_styleguide.types import (
    AnyFunctionDef,
    AnyFunctionDefAndLambda,
)

#: Function complexity counter.
FunctionCounter: TypeAlias = defaultdict[AnyFunctionDef, int]

#: Function and lambda complexity counter.
FunctionCounterWithLambda: TypeAlias = defaultdict[AnyFunctionDefAndLambda, int]

#: Function and their variables.
FunctionNames: TypeAlias = defaultdict[AnyFunctionDef, list[str]]


def _default_factory() -> FunctionCounter:
    """We use a lot of defaultdic magic in these metrics."""
    return defaultdict(int)


@final
@attr.dataclass(frozen=False)
class ComplexityMetrics:
    """
    Complexity metrics for functions.

    We use it as a store of all metrics we count in a function's body.
    There are quite a lot of them!
    """

    returns: FunctionCounter = attr.ib(factory=_default_factory)
    raises: FunctionCounter = attr.ib(factory=_default_factory)
    awaits: FunctionCounter = attr.ib(factory=_default_factory)
    asserts: FunctionCounter = attr.ib(factory=_default_factory)
    expressions: FunctionCounter = attr.ib(factory=_default_factory)
    arguments: FunctionCounterWithLambda = attr.ib(factory=_default_factory)
    variables: FunctionNames = attr.ib(factory=lambda: defaultdict(list))
