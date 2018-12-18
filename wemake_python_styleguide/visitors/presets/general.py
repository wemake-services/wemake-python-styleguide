# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast import (
    annotations,
    attributes,
    builtins,
    comparisons,
    functions,
    keywords,
    naming,
    statements,
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
    statements.StatementsWithBodiesVisitor,
    statements.WrongParametersIndentationVisitor,

    keywords.WrongRaiseVisitor,
    keywords.WrongKeywordVisitor,
    keywords.WrongComprehensionVisitor,
    keywords.WrongLoopVisitor,
    keywords.WrongTryExceptVisitor,
    keywords.WrongContextManagerVisitor,

    attributes.WrongAttributeVisitor,
    annotations.WrongAnnotationVisitor,

    functions.WrongFunctionCallVisitor,

    WrongImportVisitor,

    naming.WrongNameVisitor,
    naming.WrongModuleMetadataVisitor,
    naming.WrongVariableAssignmentVisitor,

    builtins.MagicNumberVisitor,
    builtins.WrongStringVisitor,
    builtins.WrongAssignmentVisitor,

    comparisons.WrongConditionalVisitor,
    comparisons.ComparisonSanityVisitor,
    comparisons.WrongComparisionOrderVisitor,

    # Classes:
    WrongClassVisitor,

    # Modules:
    WrongModuleNameVisitor,
    EmptyModuleContentsVisitor,
)
