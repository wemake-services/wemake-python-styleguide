from typing import Final

from wemake_python_styleguide.visitors.ast.complexity import (  # noqa: WPS235
    access,
    annotations,
    calls,
    classes,
    complex_finally,
    counts,
    function,
    imports,
    jones,
    nested,
    offset,
    overuses,
    pm,
)

#: Used to store all complexity related visitors to be later passed to checker:
PRESET: Final = (
    function.FunctionComplexityVisitor,
    function.CognitiveComplexityVisitor,
    imports.ImportMembersVisitor,
    jones.JonesComplexityVisitor,
    nested.NestedComplexityVisitor,
    offset.OffsetVisitor,
    counts.ModuleMembersVisitor,
    counts.ConditionsVisitor,
    counts.ElifVisitor,
    counts.TryExceptVisitor,
    counts.ReturnLikeStatementTupleVisitor,
    counts.TupleUnpackVisitor,
    counts.TypeParamsVisitor,
    classes.ClassComplexityVisitor,
    classes.MethodMembersVisitor,
    overuses.StringOveruseVisitor,
    overuses.ExpressionOveruseVisitor,
    access.AccessVisitor,
    calls.CallChainsVisitor,
    annotations.AnnotationComplexityVisitor,
    pm.MatchSubjectsVisitor,
    pm.MatchCasesVisitor,
    complex_finally.ComplexFinallyBlocksVisitor,
)
