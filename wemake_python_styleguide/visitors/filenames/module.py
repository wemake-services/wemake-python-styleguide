from typing_extensions import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.logic.naming.logical import alphabet, name_check
from wemake_python_styleguide.violations import naming
from wemake_python_styleguide.visitors.base import BaseFilenameVisitor


@final
class WrongModuleNameVisitor(BaseFilenameVisitor):
    """Checks that modules have correct names."""

    def visit_filename(self) -> None:
        """
        Checks a single module's filename.

        Raises:
            ConsecutiveUnderscoresInNameViolation
            PrivateNameViolation
            TooLongNameViolation
            TooShortModuleNameViolation
            TooShortNameViolation
            UnderscoredNumberNameViolation
            UnreadableNameViolation
            UnicodeNameViolation
            WrongModuleMagicNameViolation
            WrongModuleNamePatternViolation
            WrongModuleNameUnderscoresViolation
            WrongModuleNameViolation

        """
        self._check_module_name()
        self._check_module_name_length()
        self._check_module_name_pattern()
        self._check_module_name_readability()

    def _check_module_name(self) -> None:
        is_wrong_name = name_check.is_wrong_name(
            self.stem,
            constants.MODULE_NAMES_BLACKLIST,
        )
        if is_wrong_name:
            self.add_violation(naming.WrongModuleNameViolation())

        if access.is_magic(self.stem):
            if self.stem not in constants.MAGIC_MODULE_NAMES_WHITELIST:
                self.add_violation(naming.WrongModuleMagicNameViolation())

        if access.is_private(self.stem):
            self.add_violation(naming.PrivateNameViolation(text=self.stem))

        if alphabet.does_contain_unicode(self.stem):
            self.add_violation(naming.UnicodeNameViolation(text=self.stem))

    def _check_module_name_length(self) -> None:
        min_length = self.options.min_name_length
        if name_check.is_too_short_name(self.stem, min_length=min_length):
            self.add_violation(naming.TooShortNameViolation(text=self.stem))
        elif not constants.MODULE_NAME_PATTERN.match(self.stem):
            self.add_violation(naming.WrongModuleNamePatternViolation())

        max_length = self.options.max_name_length
        if name_check.is_too_long_name(self.stem, max_length=max_length):
            self.add_violation(naming.TooLongNameViolation(text=self.stem))

    def _check_module_name_pattern(self) -> None:
        if alphabet.does_contain_consecutive_underscores(self.stem):
            self.add_violation(
                naming.ConsecutiveUnderscoresInNameViolation(text=self.stem),
            )

        if alphabet.does_contain_underscored_number(self.stem):
            self.add_violation(
                naming.UnderscoredNumberNameViolation(text=self.stem),
            )

    def _check_module_name_readability(self) -> None:
        is_unreadable = alphabet.does_contain_unreadable_characters(
            self.stem,
            constants.UNREADABLE_CHARACTER_COMBINATIONS,
        )
        if is_unreadable:
            self.add_violation(
                naming.UnreadableNameViolation(text=self.stem),
            )
