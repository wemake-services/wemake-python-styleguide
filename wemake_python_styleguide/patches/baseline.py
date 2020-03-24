from collections import defaultdict
from typing import Iterable, Tuple, Type

from flake8.checker import Manager

from wemake_python_styleguide.logic import baseline


def _patch_report(manager: Type[Manager]) -> None:
    original_report = manager.report

    def report(self) -> Tuple[int, int]:  # noqa: WPS430
        # --- patch start
        saved_reports: baseline.SavedReports = defaultdict(list)
        self.saved_reports = saved_reports  # mypy requires that!
        # --- patch end

        report_result = original_report(self)

        # --- patch start
        if self.baseline is None:
            self.baseline = baseline.save_to_file(self.saved_reports)
        # --- patch end

        return report_result

    manager.report = report
    manager.baseline = baseline.load_from_file()


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
        for (error_code, line_number, column, text, physical_line) in results:
            # --- patch start
            # Here we ignore violations present in the baseline.
            if self.baseline and self.baseline.has(filename, error_code, text):
                continue

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
                self.saved_reports[filename].append(
                    (error_code, line_number, column, text, physical_line),
                )
            # --- patch end
        return reported_results_count

    manager._handle_results = _handle_results  # noqa: WPS437


def apply_patch() -> None:
    """This is the only function we export to apply all the patches."""
    _patch_report(Manager)
    _patch_handle_results(Manager)
