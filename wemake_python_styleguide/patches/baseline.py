"""
We have to patch ``flake8`` to introduce this feature.

Because there's no other way for a plugin
to be involved in a violation reporting process.

We use ``_wps_`` prefix for all properties that we apply in this patch.
"""

from collections import defaultdict
from typing import Iterable, Tuple, Type

from flake8.checker import Manager

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
        if self._wps_baseline is None:
            self._wps_baseline = baseline.write_new_file(
                self._wps_saved_reports,
            )
            show_baseline = getattr(  # Regular formatters don't have this:
                self.style_guide.formatter, 'show_baseline', None,
            )
            if show_baseline:
                show_baseline(self._wps_baseline)
        # TODO: use `--baseline-refactoring`, but it is hard
        # --- patch end

        return report_result

    manager.report = report
    manager._wps_baseline = baseline.load_from_file()  # noqa: WPS437


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
            # --- patch end
        return reported_results_count

    manager._handle_results = _handle_results  # noqa: WPS437


def apply_patch() -> None:
    """This is the only function we export to apply all the patches."""
    _patch_report(Manager)
    _patch_handle_results(Manager)
