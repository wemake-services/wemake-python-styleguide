"""
We have to patch ``flake8`` to introduce this feature.

Because there's no other way for a plugin
to be involved in a violation reporting process.

We use ``_wps_`` prefix for all properties that we apply in this patch.
"""

import sys
from collections import defaultdict
from typing import Iterable, Tuple, Type

from flake8.checker import Manager
from flake8.style_guide import Decision, StyleGuide, Violation

from wemake_python_styleguide.logic import baseline


def _patch_report(manager: Type[Manager]) -> None:
    original_report = manager.report

    def report(self) -> Tuple[int, int]:  # noqa: WPS430
        # --- patch start
        saved_reports: baseline.SavedReports = defaultdict(list)
        self._wps_saved_reports = saved_reports  # mypy requires that!
        # --- patch end

        report_result = original_report(self)

        # --- patch start
        if self.options.create_baseline:
            self._wps_baseline = baseline.write_new_file(
                self.options.baseline, self._wps_saved_reports,
            )

            formatter = self.style_guide.formatter
            formatter.write(
                '{0}Created new baseline with {1} violation(s) at:{0}{2}'.format(
                    formatter.newline,
                    self._wps_baseline.error_count(),
                    baseline.baseline_fullpath(self.options.baseline),
                ),
                None,
            )
        # TODO: use `--baseline-refactoring`, but it is hard
        # --- patch end

        return report_result

    manager.report = report


def _patch_handle_results(  # noqa: WPS210, WPS231
    manager: Type[Manager],
) -> None:
    def _handle_results(  # noqa: WPS210, WPS430
        self,
        filename: str,
        results: Iterable[baseline.CheckReport],  # noqa: WPS110
    ) -> int:
        style_guide = self.style_guide
        reported_results_count = 0

        # --- patch start
        saved_reports = self._wps_saved_reports[filename]
        # Here we ignore violations present in the baseline.
        new_ones = baseline.filter_out_saved_in_baseline(
            self._wps_baseline, results, filename,
        )
        for (error_code, line_number, column, text, physical_line) in new_ones:
            handled_error = style_guide.handle_error(
                code=error_code,
                filename=filename,
                line_number=line_number,
                column_number=column,
                text=text,
                physical_line=physical_line,
            )

            reported_results_count += handled_error

            if handled_error:
                saved_reports.append(
                    (error_code, line_number, column, text, physical_line),
                )

        if self._wps_baseline:
            self._wps_baseline.write_file(self.options.baseline)

        # We should exit successfully if created a baseline.
        return 0 if self.options.create_baseline else reported_results_count
        # --- patch end

    manager._handle_results = _handle_results  # noqa: WPS437


def _patch_start(manager: Type[Manager]) -> None:
    original_start = manager.start

    def start(self, paths=None) -> None:  # noqa: WPS430
        # --- patch start
        self._wps_baseline = None
        if self.options.create_baseline:
            if paths is not None or self.arguments:
                response = input("This will create a new baseline for only the given files. Continue? (y/n) ")
                if not response.lower().startswith("y"):
                    sys.exit(-2)
        else:
            self._wps_baseline = baseline.load_from_file(self.options.baseline)

        if self._wps_baseline is None and not self.options.create_baseline:
            print("ERROR: No baseline file found (you can create one with --create-baseline).")
            sys.exit(-2)
        # --- patch end

        original_start(self, paths)

    manager.start = start


def _patch_handle_error(style_guide: Type[StyleGuide]) -> None:
    def handle_error(
        self,
        code,
        filename,
        line_number,
        column_number,
        text,
        physical_line=None,
    ):
        disable_noqa = self.options.disable_noqa
        if not column_number:
            column_number = 0
        error = Violation(
            code,
            filename,
            line_number,
            column_number + 1,
            text,
            physical_line,
        )
        error_is_selected = (
            self.should_report_error(error.code) is Decision.Selected
        )
        is_not_inline_ignored = error.is_inline_ignored(disable_noqa) is False
        is_included_in_diff = error.is_in(self._parsed_diff)
        if (
            error_is_selected
            and is_not_inline_ignored
            and is_included_in_diff
        ):
            # --- patch start
            # Suppress output when creating baseline, we only want a summary.
            if not self.options.create_baseline:
                self.formatter.handle(error)
                self.stats.record(error)
            # --- patch end
            return 1
        return 0

    style_guide.handle_error = handle_error


def apply_patch() -> None:
    """This is the only function we export to apply all the patches."""
    _patch_report(Manager)
    _patch_handle_results(Manager)
    _patch_start(Manager)
    _patch_handle_error(StyleGuide)
