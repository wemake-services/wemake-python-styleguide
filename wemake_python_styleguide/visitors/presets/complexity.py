# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast.complexity import (
    counts,
    function,
    jones,
    nested,
    offset,
)

#: Used to store all complexity related visitors to be later passed to checker:
COMPLEXITY_PRESET = (
    function.FunctionComplexityVisitor,
    jones.JonesComplexityVisitor,
    nested.NestedComplexityVisitor,
    offset.OffsetVisitor,
    counts.ImportMembersVisitor,
    counts.ModuleMembersVisitor,
    counts.MethodMembersVisitor,
    counts.ConditionsVisitor,
)
