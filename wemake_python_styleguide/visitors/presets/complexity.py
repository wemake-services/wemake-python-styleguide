# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ImportMembersVisitor,
    MethodMembersVisitor,
    ModuleMembersVisitor,
)
from wemake_python_styleguide.visitors.ast.complexity.function import (
    FunctionComplexityVisitor,
)
from wemake_python_styleguide.visitors.ast.complexity.jones import (
    JonesComplexityVisitor,
)
from wemake_python_styleguide.visitors.ast.complexity.nested import (
    NestedComplexityVisitor,
)
from wemake_python_styleguide.visitors.ast.complexity.offset import (
    OffsetVisitor,
)

#: Used to store all complexity related visitors to be later passed to checker:
COMPLEXITY_PRESET = (
    FunctionComplexityVisitor,
    NestedComplexityVisitor,
    OffsetVisitor,
    ImportMembersVisitor,
    ModuleMembersVisitor,
    MethodMembersVisitor,
    JonesComplexityVisitor,
)
