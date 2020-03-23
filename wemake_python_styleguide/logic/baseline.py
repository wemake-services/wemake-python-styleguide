import json
import os
from collections import Counter, defaultdict
from hashlib import md5
from typing import DefaultDict, Dict, Iterable, List, Mapping, Optional, Tuple

import attr
from typing_extensions import Final, final

#: That's a constant filename where we store our baselines.
_BASELINE_FILE: Final = '.flake8-baseline.json'

#: Content is: `error_code, line_number, column, text, physical_line`.
CheckReport = Tuple[str, int, int, str, str]

#: Mapping of filename and the report result.
SavedReports = Dict[str, List[CheckReport]]


def _baseline_fullpath() -> str:
    """We only store baselines in the current (main) directory."""
    return os.path.join(os.curdir, _BASELINE_FILE)


def _unique_paths_converter(
    mapping: Mapping[str, Iterable[str]],
) -> Mapping[str, Dict[str, int]]:
    return {
        path: Counter(violations)
        for path, violations in mapping.items()
    }


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

    paths: Mapping[str, Dict[str, int]] = attr.ib(
        converter=_unique_paths_converter,
    )

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
