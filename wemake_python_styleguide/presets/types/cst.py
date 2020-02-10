# -*- coding: utf-8 -*-

from typing_extensions import Final

from wemake_python_styleguide.visitors.cst import attributes

#: Used to store all token related visitors to be later passed to checker:
PRESET: Final = (
    attributes.AttributeCSTVisitor,
)
