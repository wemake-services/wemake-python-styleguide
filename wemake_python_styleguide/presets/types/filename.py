from typing_extensions import Final

from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)

#: Here we define all filename-based visitors.
PRESET: Final = (
    WrongModuleNameVisitor,
)
