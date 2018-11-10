# -*- coding: utf-8 -*-

from wemake_python_styleguide import constants
from wemake_python_styleguide.logics.naming import access, logical
from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.naming import (
    ConsecutiveUnderscoresInNameViolation,
    PrivateNameViolation,
    TooLongNameViolation,
    TooShortNameViolation,
    UnderscoredNumberNameViolation,
    UnicodeNameViolation,
    WrongModuleMagicNameViolation,
    WrongModuleNamePatternViolation,
    WrongModuleNameViolation,
)
from wemake_python_styleguide.visitors.base import BaseFilenameVisitor


@final
class WrongModuleNameVisitor(BaseFilenameVisitor):
    """Checks that modules have correct names."""

    def _check_module_name(self) -> None:
        if logical.is_wrong_name(self.stem, constants.MODULE_NAMES_BLACKLIST):
            self.add_violation(WrongModuleNameViolation())

        if access.is_magic(self.stem):
            if self.stem not in constants.MAGIC_MODULE_NAMES_WHITELIST:
                self.add_violation(WrongModuleMagicNameViolation())

        if access.is_private(self.stem):
            self.add_violation(PrivateNameViolation(text=self.stem))

        if logical.does_contain_unicode(self.stem):
            self.add_violation(UnicodeNameViolation(text=self.stem))

    def _check_module_name_length(self) -> None:
        min_length = self.options.min_name_length
        if logical.is_too_short_name(self.stem, min_length=min_length):
            self.add_violation(TooShortNameViolation(text=self.stem))

        max_length = self.options.max_name_length
        if logical.is_too_long_name(self.stem, max_length=max_length):
            self.add_violation(TooLongNameViolation(text=self.stem))

    def _check_module_name_pattern(self) -> None:
        if not constants.MODULE_NAME_PATTERN.match(self.stem):
            self.add_violation(WrongModuleNamePatternViolation())

        if logical.does_contain_consecutive_underscores(self.stem):
            self.add_violation(
                ConsecutiveUnderscoresInNameViolation(text=self.stem),
            )

        if logical.does_contain_underscored_number(self.stem):
            self.add_violation(UnderscoredNumberNameViolation(text=self.stem))

    def visit_filename(self) -> None:
        """
        Checks a single module's filename.

        Raises:
            TooShortModuleNameViolation
            WrongModuleMagicNameViolation
            WrongModuleNameViolation
            WrongModuleNamePatternViolation
            WrongModuleNameUnderscoresViolation
            UnderscoredNumberNameViolation
            TooLongNameViolation

        """
        self._check_module_name()
        self._check_module_name_length()
        self._check_module_name_pattern()
