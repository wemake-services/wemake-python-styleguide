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

    WrongFunctionCallVisitor,
    WrongImportVisitor,

    naming.WrongNameVisitor,
    naming.WrongModuleMetadataVisitor,

    numbers.MagicNumberVisitor,
    WrongStringVisitor,

    comparisons.ConstantComparisonVisitor,
    comparisons.WrongOrderVisitor,
    comparisons.MultipleInVisitor,

    # Classes:
    WrongClassVisitor,

    # Modules:
    WrongModuleNameVisitor,
    EmptyModuleContentsVisitor,
)
