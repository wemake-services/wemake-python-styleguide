# -*- coding: utf-8 -*-

from wemake_python_styleguide import constants
from wemake_python_styleguide.logics import filenames
from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.naming import (
    TooShortModuleNameViolation,
    UnderScoredNumberNameViolation,
    WrongModuleMagicNameViolation,
    WrongModuleNamePatternViolation,
    WrongModuleNameUnderscoresViolation,
    WrongModuleNameViolation,
)
from wemake_python_styleguide.visitors.base import BaseFilenameVisitor


@final
class WrongModuleNameVisitor(BaseFilenameVisitor):
    """Checks that modules have correct names."""

    def _check_module_name(self) -> None:
        is_wrong_name = filenames.is_stem_in_list(
            self.filename,
            constants.MODULE_NAMES_BLACKLIST,
        )
        if is_wrong_name:
            self.add_violation(WrongModuleNameViolation())

    def _check_magic_name(self) -> None:
        if filenames.is_magic(self.filename):
            good_magic = filenames.is_stem_in_list(
                self.filename,
                constants.MAGIC_MODULE_NAMES_WHITELIST,
            )
            if not good_magic:
                self.add_violation(WrongModuleMagicNameViolation())

    def _check_module_name_length(self) -> None:
        is_short = filenames.is_too_short_stem(
            self.filename,
            min_length=self.options.min_module_name_length,
        )
        if is_short:
            self.add_violation(TooShortModuleNameViolation())

    def _check_module_name_pattern(self) -> None:
        if not filenames.is_matching_pattern(self.filename):
            self.add_violation(WrongModuleNamePatternViolation())

    def _check_underscores(self) -> None:
        repeating_underscores = self.filename.count('__')
        if filenames.is_magic(self.filename):
            repeating_underscores -= 2
        if repeating_underscores > 0:
            self.add_violation(WrongModuleNameUnderscoresViolation())

    def _check_underscored_numbers(self) -> None:
        if not filenames.is_stem_with_underscored_number(self.filename):
            self.add_violation(UnderScoredNumberNameViolation())

    def visit_filename(self) -> None:
        """
        Checks a single module's filename.

        Raises:
            TooShortModuleNameViolation
            WrongModuleMagicNameViolation
            WrongModuleNameViolation
            WrongModuleNamePatternViolation
            WrongModuleNameUnderscoresViolation
            UnderScoredNumberNameViolation

        """
        self._check_module_name()
        self._check_magic_name()
        self._check_module_name_length()
        self._check_module_name_pattern()
        self._check_underscores()
        self._check_underscored_numbers()
