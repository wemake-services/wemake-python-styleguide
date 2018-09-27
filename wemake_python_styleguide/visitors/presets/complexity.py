# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast.complexity import (
    counts,
    function,
    jones,
    nested,
    numbers,
    offset,
)

#: Used to store all complexity related visitors to be later passed to checker:
COMPLEXITY_PRESET = (
    function.FunctionComplexityVisitor,
    jones.JonesComplexityVisitor,
    nested.NestedComplexityVisitor,
    numbers.MagicNumberVisitor,
    offset.OffsetVisitor,
    counts.ImportMembersVisitor,
    counts.ModuleMembersVisitor,
    counts.MethodMembersVisitor,
    counts.ConditionsVisitor,
)
