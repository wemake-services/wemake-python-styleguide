from typing import Final

from wemake_python_styleguide.visitors.filenames.module import (
    WrongModuleNameVisitor,
)

PRESET: Final = (WrongModuleNameVisitor,)
"""Here we define all filename-based visitors."""
