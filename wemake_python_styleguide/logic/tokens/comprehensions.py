import tokenize
from typing import List, Optional

import attr
from typing_extensions import final


@final
@attr.dataclass(slots=True)
class Compehension(object):
    """
    Represents a syntax for Python comprehension.

    The optimal way of using this class is
    by just creating it with the first opening ``left_bracket``
    and then assigning values you need when you meet them.
    """

    left_bracket: tokenize.TokenInfo
    expr: Optional[tokenize.TokenInfo] = None

    # `for` keywords
    fors: List[tokenize.TokenInfo] = attr.ib(factory=list)

    # `in` part, keywords and expressions
    ins: List[tokenize.TokenInfo] = attr.ib(factory=list)
    in_exprs: List[tokenize.TokenInfo] = attr.ib(factory=list)

    # Condition part:
    _ifs: List[tokenize.TokenInfo] = attr.ib(factory=list)

    async_broken: bool = False
    _checked: bool = False

    def append_if(self, token: tokenize.TokenInfo) -> None:
        """
        Conditionally appends ``if`` token, if there's at least one ``for``.

        Why? Because you might have ``if`` before ``for``.
        In this case it is just a ternary inside ``expr``.
        In real comprehensions ``if`` are always after ``for``.
        """
        if self.fors:
            self._ifs.append(token)

    def is_ready(self) -> bool:
        """
        Checks that comprehension is built correctly with all required parts.

        We also check that each compehension is analyzed only once.
        """
        return (
            self.expr is not None and
            bool(self.fors) and
            len(self.fors) == len(self.ins) == len(self.in_exprs) and
            not self._checked
        )

    def is_valid(self) -> bool:
        """Checks that compehension definition is valid."""
        if self.async_broken:
            return False

        for_in = self._check_for_in()

        # mypy requires this `assert`, always true if `is_ready()`
        assert self.expr  # noqa: S101

        is_multiline = self.expr.start[0] != self._first_for_line
        fors = self._check_fors(is_multiline=is_multiline)
        for_if = self._check_for_if(is_multiline=is_multiline)

        self._checked = True  # noqa: WPS601
        return for_in and fors and for_if

    @property
    def _first_for_line(self) -> int:
        """Returns the line number of the first ``for`` token."""
        return self.fors[0].start[0]

    def _check_for_in(self) -> bool:
        """Checks that all ``for`` and ``in`` tokens are aligned together."""
        return all(
            for_.start[0] == in_.start[0] == in_expr.start[0]
            for for_, in_, in_expr in zip(self.fors, self.ins, self.in_exprs)
        )

    def _check_fors(self, *, is_multiline: bool) -> bool:
        """Checks that all ``for`` tokens are aligned."""
        if len(self.fors) == 1:
            return True  # one `for` is always correct

        if is_multiline:
            return all(
                for_.start[0] == self._first_for_line + index
                for index, for_ in enumerate(self.fors)
                if index > 0
            )
        return all(
            for_.start[0] == self._first_for_line
            for for_ in self.fors
        )

    def _check_for_if(self, *, is_multiline: bool) -> bool:
        """Checks that all ``for`` and ``if`` tokens are aligned."""
        if is_multiline:
            last_for_line = self.fors[-1].start[0]
            return all(
                if_.start[0] == last_for_line + index + 1
                for index, if_ in enumerate(self._ifs)
            )
        return all(
            if_.start[0] == self._first_for_line
            for if_ in self._ifs
        )
