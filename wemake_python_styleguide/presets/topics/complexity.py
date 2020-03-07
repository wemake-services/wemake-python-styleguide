from typing_extensions import Final

from wemake_python_styleguide.visitors.ast.complexity import (  # noqa: WPS235
    access,
    annotations,
    calls,
    classes,
    counts,
    function,
    jones,
    nested,
    offset,
    overuses,
)

#: Used to store all complexity related visitors to be later passed to checker:
PRESET: Final = (
    function.FunctionComplexityVisitor,
    function.CognitiveComplexityVisitor,

    jones.JonesComplexityVisitor,

    nested.NestedComplexityVisitor,

    offset.OffsetVisitor,

    counts.ImportMembersVisitor,
    counts.ModuleMembersVisitor,
    counts.ConditionsVisitor,
    counts.ElifVisitor,
    counts.TryExceptVisitor,
    counts.YieldTupleVisitor,

    classes.ClassComplexityVisitor,
    classes.MethodMembersVisitor,

    overuses.StringOveruseVisitor,
    overuses.ExpressionOveruseVisitor,

    access.AccessVisitor,

    calls.CallChainsVisitor,

    annotations.AnnotationComplexityVisitor,
)
