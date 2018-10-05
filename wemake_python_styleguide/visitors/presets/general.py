# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast import keywords, naming, numbers
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor
from wemake_python_styleguide.visitors.ast.comparisons import (
    ConstantComparisonVisitor,
)
from wemake_python_styleguide.visitors.ast.functions import (
    WrongFunctionCallVisitor,
)
from wemake_python_styleguide.visitors.ast.imports import WrongImportVisitor
from wemake_python_styleguide.visitors.ast.modules import WrongContentsVisitor
from wemake_python_styleguide.visitors.ast.strings import WrongStringVisitor
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
    WrongModuleNameVisitor,
)

#: Used to store all general visitors to be later passed to checker:
GENERAL_PRESET = (
    # General:
    keywords.WrongRaiseVisitor,
    keywords.WrongKeywordVisitor,
    WrongFunctionCallVisitor,
    WrongImportVisitor,
    naming.WrongNameVisitor,
    naming.WrongModuleMetadataVisitor,
    numbers.MagicNumberVisitor,
    WrongStringVisitor,
    WrongContentsVisitor,
    ConstantComparisonVisitor,

    # Classes:
    WrongClassVisitor,

    # Modules:
    WrongModuleNameVisitor,
)
