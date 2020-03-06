import tokenize
from typing import ClassVar, FrozenSet

from typing_extensions import final

from wemake_python_styleguide.violations.refactoring import (
    ImplicitElifViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


@final
class IfElseVisitor(BaseTokenVisitor):
    """
    Checks if tokens tokens.

    We use ``tokenize`` instead of ``ast`` because

    .. code:: python

       if some:
           ...
        else:
            if other:
                ...

    has the same ``ast`` representation as:

    .. code:: python

      if some:
          ...
      elif other:
          ...

    That's why we have to use ``tokenize`` to find
    the raw tokens inside the text.

    """

    _allowed_token_types: ClassVar[FrozenSet[int]] = frozenset((
        tokenize.NEWLINE,
        tokenize.NL,
        tokenize.COLON,
        tokenize.INDENT,
    ))

    def visit_name(self, token: tokenize.TokenInfo) -> None:
        """
        Checks that ``if`` nodes are defined correctly.

        Raises:
            ImplicitElifViolation

        """
        self._check_implicit_elif(token)

    def _does_else_belong_to_if(self, start_index: int) -> bool:
        previous_token = self.file_tokens[start_index - 1]

        if previous_token.type != tokenize.DEDENT:
            # This is not the first token on the line, which means that it can
            # also be "embedded" else: x if A else B
            return False

        for token in reversed(self.file_tokens[:start_index - 1]):
            if token.type != tokenize.NAME:
                continue

            # Here we rely upon an intuition that in Python else have to be
            # on the same level (same indentation) as parent statement.
            if token.start[1] == previous_token.start[1]:
                return token.string in {'if', 'elif'}

        return False

    def _check_implicit_elif(self, token: tokenize.TokenInfo) -> None:
        if token.string != 'else':
            return

        index = self.file_tokens.index(token)

        # `else` token can belong also to `for` and `try/except` statement,
        # which can trigger false positive for that violation.
        if not self._does_else_belong_to_if(index):
            return

        # There's a bug in coverage, I am not sure how to make it work.
        for next_token in self.file_tokens[index + 1:]:  # pragma: no cover
            if next_token.exact_type in self._allowed_token_types:
                continue
            elif next_token.string == 'if':
                self.add_violation(ImplicitElifViolation(next_token))
            return
