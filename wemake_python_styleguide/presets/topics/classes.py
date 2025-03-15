from typing import Final

from wemake_python_styleguide.visitors.ast.classes import (
    attributes,
    classdef,
    methods,
)

#: Used to store all classes related visitors to be later passed to checker:
PRESET: Final = (
    classdef.WrongClassDefVisitor,
    classdef.WrongClassBodyVisitor,
    attributes.ClassAttributeVisitor,
    attributes.WrongSlotsVisitor,
    methods.WrongMethodVisitor,
    methods.ClassMethodOrderVisitor,
    methods.BuggySuperCallVisitor,
    classdef.ConsecutiveDefaultTypeVarsVisitor,
)
