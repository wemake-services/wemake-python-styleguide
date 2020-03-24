"""
Baselines allow us to adopt this linter incrementally.

You can start using it with just a single command!

.. code:: bash

    flake8 --baseline your_module

This guide will explain how it works.

Steps
~~~~~

There are several steps in how baseline works.

We can run the linter with ``--baseline`` mode enabled.
What will happen?

If you don't have ``.flake8-baseline.json``,
then a new one will be created containing all the violations you have.

If you already have ``.flake8-baseline.json`` file,
than your pre-saved violations will be ignored.

However, new violations will still be reported.

Updating baseline
~~~~~~~~~~~~~~~~~

To update a baseline you can delete the old one:

.. code:: bash

    rm .flake8-baseline.json

And create a new one with ``--baseline`` flag.

Baseline contents
~~~~~~~~~~~~~~~~~

Things we care when working with baselines:

1. Violation codes and text descriptions
2. Filenames

When these values change
(for example: file is renamed or violation code is changed),
we will treat these violations as new ones.
And report them to the user as usual.

Things we don't care when working with baselines:

1. Violation locations, because lines and columns
   can be easily changed by simple refactoring
2. Activated plugins
3. Config values
4. Target files and directories

So, when you add new plugins or change any config values,
then you might want ot update the baseline as well.

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
