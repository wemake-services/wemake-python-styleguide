# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast import (
    comparisons,
    keywords,
    naming,
    numbers,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallVisitor,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor
from wemake_python_styleguide.visitors.ast.modules import (
    EmptyModuleContentsVisitor,
)
from wemake_python_styleguide.visitors.ast.strings import WrongStringVisitor
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
    WrongModuleNameVisitor,
)

#: Used to store all general visitors to be later passed to checker:
GENERAL_PRESET = (
    # General:
    keywords.WrongRaiseVisitor,
    keywords.WrongKeywordVisitor,
    keywords.WrongListComprehensionVisitor,
    keywords.WrongForElseVisitor,
    keywords.WrongTryFinallyVisitor,

    WrongFunctionCallVisitor,
    WrongImportVisitor,

    naming.WrongNameVisitor,
    naming.WrongModuleMetadataVisitor,
    naming.WrongVariableAssignmentVisitor,

    numbers.MagicNumberVisitor,
    WrongStringVisitor,

    comparisons.WrongConditionalVisitor,
    comparisons.ComparisonSanityVisitor,
    comparisons.WrongComparisionOrderVisitor,

    # Classes:
    WrongClassVisitor,

    # Modules:
    WrongModuleNameVisitor,
    EmptyModuleContentsVisitor,
)
