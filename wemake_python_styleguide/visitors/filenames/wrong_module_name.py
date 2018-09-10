# -*- coding: utf-8 -*-

from wemake_python_styleguide.constants import (
    BAD_MODULE_NAMES,
    MAGIC_MODULE_NAMES_WHITELIST,
)
from wemake_python_styleguide.errors.modules import (
    TooShortModuleNameViolation,
    WrongModuleMagicNameViolation,
    WrongModuleNameViolation,
)
from wemake_python_styleguide.logics.filenames import (
    is_magic,
    is_stem_in_list,
    is_too_short_stem,
)
from wemake_python_styleguide.visitors.base import BaseFilenameVisitor


class WrongModuleNameVisitor(BaseFilenameVisitor):
    """Checks that modules have correct names."""

    def _check_module_name(self) -> None:
        if is_stem_in_list(self.filename, BAD_MODULE_NAMES):
            self.add_error(WrongModuleNameViolation())

    def _check_magic_name(self) -> None:
        if is_magic(self.filename):
            good_magic = is_stem_in_list(
                self.filename,
                MAGIC_MODULE_NAMES_WHITELIST,
            )
            if not good_magic:
                self.add_error(WrongModuleMagicNameViolation())

    def _check_module_name_length(self) -> None:
        is_short = is_too_short_stem(
            self.filename,
            min_length=self.options.min_module_name_length,
        )
        if is_short:
            self.add_error(TooShortModuleNameViolation())

    def visit_filename(self) -> None:
        """
        Checks a single module's filename.

        Raises:
            TooShortModuleNameViolation
            WrongModuleMagicNameViolation
            WrongModuleNameViolation

        """
        self._check_module_name()
        self._check_magic_name()
        self._check_module_name_length()
