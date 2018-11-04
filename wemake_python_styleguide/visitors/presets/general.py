# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast import (
    attributes,
    builtins,
    comparisons,
    functions,
    keywords,
    naming,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor
from wemake_python_styleguide.visitors.ast.modules import (
    EmptyModuleContentsVisitor,
)
from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)

#: Used to store all general visitors to be later passed to checker:
GENERAL_PRESET = (
    # General:
    keywords.WrongRaiseVisitor,
    keywords.WrongKeywordVisitor,
    keywords.WrongComprehensionVisitor,
    keywords.WrongLoopVisitor,
    keywords.WrongTryExceptVisitor,

    attributes.WrongAttributeVisitor,

    functions.WrongFunctionCallVisitor,
    functions.FunctionDefinitionVisitor,

    WrongImportVisitor,

    naming.WrongNameVisitor,
    naming.WrongModuleMetadataVisitor,
    naming.WrongVariableAssignmentVisitor,

    builtins.MagicNumberVisitor,
    builtins.WrongStringVisitor,

    comparisons.WrongConditionalVisitor,
    comparisons.ComparisonSanityVisitor,
    comparisons.WrongComparisionOrderVisitor,

    # Classes:
    WrongClassVisitor,

    # Modules:
    WrongModuleNameVisitor,
    EmptyModuleContentsVisitor,
)
