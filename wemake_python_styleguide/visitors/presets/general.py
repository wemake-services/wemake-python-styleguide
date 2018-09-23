# -*- coding: utf-8 -*-

from wemake_python_styleguide.visitors.ast.general.wrong_function_call import (
    WrongFunctionCallVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_import import (
    WrongImportVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_keyword import (
    WrongKeywordVisitor,
    WrongRaiseVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_module import (
    WrongContentsVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_name import (
    WrongModuleMetadataVisitor,
    WrongNameVisitor,
)
from wemake_python_styleguide.visitors.ast.general.wrong_string import (
    WrongStringVisitor,
)
from wemake_python_styleguide.visitors.ast.wrong_class import WrongClassVisitor
from wemake_python_styleguide.visitors.filenames.wrong_module_name import (
    WrongModuleNameVisitor,
)

#: Used to store all general visitors to be later passed to checker:
GENERAL_PRESET = (
    # General:
    WrongRaiseVisitor,
    WrongFunctionCallVisitor,
    WrongImportVisitor,
    WrongKeywordVisitor,
    WrongNameVisitor,
    WrongModuleMetadataVisitor,
    WrongStringVisitor,
    WrongContentsVisitor,

    # Classes:
    WrongClassVisitor,

    # Modules:
    WrongModuleNameVisitor,
)
