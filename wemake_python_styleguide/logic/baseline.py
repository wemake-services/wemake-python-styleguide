import datetime as dt
import json
import os
from collections import defaultdict
from typing import NamedTuple
from typing import DefaultDict, Dict, Iterable, List, Mapping, Optional, Tuple

import attr
from typing_extensions import Final, TypedDict, final

#: That's a constant filename where we store our baselines.
BASELINE_FILE: Final = '.flake8-baseline.json'

#: We version baseline files independenly. Because we can break things.
BASELINE_FILE_VERSION: Final = '1'

#: Content is: `error_code, line_number, column, text, physical_line`.
CheckReport = Tuple[str, int, int, str, str]

#: This is how we identify the violation.
ViolationKey = Tuple[str, str]

#: Mapping of filename and the report result.
SavedReports = Dict[str, List[CheckReport]]

_BaselineMetadata = NamedTuple('_BaselineMetadata', [
    ('created_at', str),
    ('updated_at', str),
    ('baseline_file_version', str),
])

_BaselineEntry = NamedTuple('_BaselineEntry', [
    ('error_code', str),
    ('line', int),
    ('column', int),
    ('message', str),
    ('physical_line', str),
])


@final
@attr.dataclass(slots=True, frozen=True)
class _BaselineFile(object):
    """
    Baseline file representation.

    How paths are stored?
    We use ``path`` -> ``violations`` mapping.
    """

    metadata: _BaselineMetadata
    paths: Mapping[str, List[_BaselineEntry]]
    _db: Mapping[str, Mapping[str, List[_BaselineEntry]]] = attr.ib(
        init=False,
        hash=False,
        eq=False,
        repr=False,
    )

    def __attrs_post_init__(self) -> None:
        """Builds a mutable database of known violations."""
        object.__setattr__(self, '_db', {})
        for filename, violations in self.paths.items():
            grouped: DefaultDict[
                str, _BaselineEntry,
            ] = defaultdict(list)
            for one in violations:
                grouped[one[0]].append(one)
            self._db.update({filename: grouped})

    def filter_group(
        self,
        filename: str,
        violation_key: str,
        violations: List[CheckReport],
    ) -> List[CheckReport]:
        """
        Tells whether or not this violation is saved in the baseline.

        It uses several attempts to guess which violation is which. Why?
        Because one can move the violation upwards or downwards
        in the source code, but it will stay exactly the same.
        Or one can slightly modify the source code of the line,
        but leave it in the same place.

        We do realize that there would be some rear cases
        that old violations will be reported instead of new ones sometimes.
        But that's fine. Probably there's no determenistic algorithm for it.
        """
        db_file = self._db.get(filename, {})
        candidates = db_file.get(violation_key, None)
        if not candidates:  # when we don't have any stored violations
            return violations  # we just return all reported violations
        candidates = candidates[:]

        # algorithm:
        # 1. find exact matches, remove them from being reported
        # 2. delete exact matches from the db
        # 3. start fuzzy match by `physical_line` and `line`
        # 4. delete fuzzy matches from the db
        # 5. start fuzzy match by `column` and `line`
        # 6. delete fuzzy matches from the db
        # 7. start fuzzy matches by `physical_line`
        # 8. delete fuzzy matches from the db

        matchers = [
            [1, 2, 4],
            [1, 4],
            [2, 4],
            [1, 2],
            [4],
        ]

        def x(args):
            def factory(c, v):
                return all(c[a] == v[a] for a in args)
            return factory

        for matcher in matchers:
            ignored_violations = []
            for violation in violations:
                b = self._try_match(candidates, violation, x(matcher))
                if b:
                    ignored_violations.append(violation)
                    # Update our baseline, to keep in sync with codebase.
                    db_file[violation_key].remove(b)
                    db_file[violation_key].append(violation)
            for ignored_violation in ignored_violations:
                violations.remove(ignored_violation)

        # Unused candidates should be removed.
        for c in candidates:
            db_file[violation_key].remove(c)
        # Completely remove the key if no violations left.
        if not db_file[violation_key]:
            db_file.pop(violation_key)

        return violations

    def _try_match(self, candidates, violation, matcher) -> Optional[_BaselineEntry]:
        used_candidate = None
        for candidate in candidates:
            if matcher(candidate, violation):
                used_candidate = candidate
                break

        if used_candidate is not None:
            candidates.remove(used_candidate)
            return used_candidate
        return None

    def remove_unused_keys(self, filename: str, used_keys: Iterable[str]) -> None:
        """Remove unused keys for filename from the baseline."""
        db_file = self._db.get(filename)
        if db_file is None:
            return

        unused_keys = db_file.keys() - used_keys
        for k in unused_keys:
            db_file.pop(k)
        # Completely remove file if no violations left.
        if not db_file:
            self._db.pop(filename)

    def error_count(self) -> int:
        """Return the error count that is stored in the baseline."""
        return sum(len(per_file) for per_file in self.paths.values())

    def write_file(self, filename: str) -> None:
        """Write this baseline to filename."""
        self._update_paths_from_db()

        baseline_data = attr.asdict(
            self,
            # We don't need to dump private and protected attributes.
            filter=lambda attrib, _: not attrib.name.startswith('_'),
        )
        with open(baseline_fullpath(filename), 'w') as baseline_file:
            json.dump(
                baseline_data,
                baseline_file,
                sort_keys=True,
                indent=2,
            )

    def _update_paths_from_db(self):
        self.paths.clear()
        for filename, groups in self._db.items():
            self.paths[filename] = [v for v_list in groups.values() for v in v_list]

    @classmethod
    def from_report(
        cls,
        saved_reports: SavedReports,
    ) -> '_BaselineFile':
        """Factory method to construct baselines from ``flake8`` reports."""
        paths: DefaultDict[str, List[_BaselineEntry]] = defaultdict(list)
        for filename, reports in saved_reports.items():
            for report in reports:
                paths[filename].append(report)

        now = dt.datetime.now().isoformat()
        return cls(
            _BaselineMetadata(now, now, BASELINE_FILE_VERSION),
            paths,
        )


def filter_out_saved_in_baseline(
    baseline: Optional[_BaselineFile],
    reported: Iterable[CheckReport],
    filename: str,
) -> Iterable[CheckReport]:
    """We don't need to report violations saved in the baseline."""
    if baseline is None:
        return reported  # baseline does not exist yet, return everything

    new_results = []  # TODO list comp

    grouped = defaultdict(list)
    for check_report in reported:
        grouped[check_report[0]].append(check_report)

    for violation_key, violations in grouped.items():
        new_results.extend(baseline.filter_group(
            filename, violation_key, violations,
        ))

    baseline.remove_unused_keys(filename, grouped.keys())

    return new_results


def baseline_fullpath(filename: str) -> str:
    """We only store baselines in the current (main) directory."""
    return os.path.join(os.curdir, filename)


def load_from_file(filename: str) -> Optional[_BaselineFile]:
    """
    Loads baseline ``json`` files from current workdir.

    It might return ``None`` when file does not exist.
    It means, that we run ``--baseline`` for the very first time.
    """
    try:
        with open(baseline_fullpath(filename)) as baseline_file:
            return _BaselineFile(**json.load(baseline_file))
    except IOError:  # There was probably no baseline file, that's ok.
        return None  # We will create a new one later.


def write_new_file(
    filename: str, saved_reports: SavedReports,
) -> _BaselineFile:
    """Creates and writes new baseline ``json`` file in current workdir."""
    baseline = _BaselineFile.from_report(saved_reports)
    baseline.write_file(filename)
    return baseline
