import json
import os
import datetime as dt
from collections import Counter, defaultdict
from typing import DefaultDict, Dict, Iterable, List, Mapping, Optional, Tuple

import attr
from typing_extensions import Final, final, TypedDict

#: That's a constant filename where we store our baselines.
BASELINE_FILE: Final = '.flake8-baseline.json'

#: Content is: `error_code, line_number, column, text, physical_line`.
CheckReport = Tuple[str, int, int, str, str]

#: Mapping of filename and the report result.
SavedReports = Dict[str, List[CheckReport]]


def _baseline_fullpath() -> str:
    """We only store baselines in the current (main) directory."""
    return os.path.join(os.curdir, BASELINE_FILE)


def _unique_paths_converter(
    mapping: Mapping[str, Iterable[str]],
) -> Mapping[str, Dict[str, int]]:
    return {
        path: Counter(violations)
        for path, violations in mapping.items()
    }


@final
class _BaselineMetadata(TypedDict):
    """This class stores metadata that was used to create the baseline."""

    baseline_file_version: str
    created_at: dt.datetime
    updated_at: dt.datetime


@final
class _BaselineEntry(TypedDict):
    """Represents internal violation structure that is used for recordings."""

    error_code: str
    message: str
    line: int
    column: int
    physical_line: str


@final
@attr.dataclass(slots=True, frozen=True)
class _BaselineFile(object):
    """
    Baseline file representation.

    How paths are stored?
    We use ``path`` -> ``violations`` mapping, here ``violations`` is
    a mutable dict of ``digest`` and ``count``.

    We mutate ``count`` to mark violation as found.
    Once there are no more violations to find in the baseline,
    we start to report them!

    """

    metadata: _BaselineMetadata
    paths: Mapping[str, List[_BaselineEntry]]

    def filter_baseline(
        self,
        violations: List[CheckReport],
    ) -> List[CheckReport]:
        groupped_by_code = self._group_by_code(violations)
        filtered_violations = []

        for violation in violations:
            same_codes = groupped_by_code.get(error_code)
            if same_codes and self._should_be_ignored(violation, same_codes):
                continue

            filtered_violations.append(violation)
        return violation

    def _should_be_ignored(
        self,
        violation: CheckResult,
        similar_violations: List[CheckReport],
    ]) -> bool:
        # TODO: here we decide whether this violation should be ignored
        # or any other from the list.
        return False

    def has(self, filename: str, error_code: str, text: str) -> bool:
        """
        Tells whether or not this violation is saved in the baseline.

        This operation is impure. Because we mutate the object's state.
        After we find a violation once, it's counter is decreased.
        That's how we controll violations' count inside a single file.
        """
        if filename not in self.paths:
            return False

        per_file = self.paths[filename]
        digest = self._generate_violation_hash(error_code, text)

        per_file[digest] = per_file[digest] - 1
        return per_file[digest] >= 0

    @classmethod
    def from_report(
        cls, saved_reports: SavedReports,
    ) -> '_BaselineFile':
        """Factory method to construct baselines from ``flake8`` like stats."""
        paths: DefaultDict[str, List[str]] = defaultdict(list)

        for filename, reports in saved_reports.items():
            for report in reports:
                paths[filename].append(
                    cls._generate_violation_hash(report[0], report[3]),
                )
        return cls(paths)

    @classmethod
    def _generate_violation_hash(cls, error_code: str, message: str) -> str:
        digest = md5()  # noqa: S303
        digest.update(error_code.encode())
        digest.update(message.encode())
        return digest.hexdigest()


def load_from_file() -> Optional[_BaselineFile]:
    """
    Loads baseline ``json`` files from current workdir.

    It might return ``None`` when file does not exist.
    It means, that we run ``--baseline`` for the very first time.
    """
    try:
        with open(_baseline_fullpath()) as baseline_file:
            return _BaselineFile(**json.load(baseline_file))
    except IOError:
        # There was probably no baseline file, that's ok.
        # We will create a new one later.
        return None


def save_to_file(saved_reports: SavedReports) -> _BaselineFile:
    """Creates new baseline ``json`` files in current workdir."""
    baseline = _BaselineFile.from_report(saved_reports)
    with open(_baseline_fullpath(), 'w') as baseline_file:
        json.dump(
            attr.asdict(baseline),
            baseline_file,
            sort_keys=True,
            indent=2,
        )

    return baseline
