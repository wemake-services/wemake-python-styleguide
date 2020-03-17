import ast
import re
import string
from collections import Counter, Hashable, defaultdict
from contextlib import suppress
from typing import (
    ClassVar,
    DefaultDict,
    FrozenSet,
    Iterable,
    List,
    Optional,
    Sequence,
    Union,
)
from typing.re import Pattern

from typing_extensions import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.compat.aliases import (
    AssignNodesWithWalrus,
    FunctionNodes,
    TextNodes,
)
from wemake_python_styleguide.logic import nodes, safe_eval, source
from wemake_python_styleguide.logic.naming.name_nodes import extract_name
from wemake_python_styleguide.logic.tree import operators, strings
from wemake_python_styleguide.types import AnyFor, AnyNodes, AnyText, AnyWith
from wemake_python_styleguide.violations import best_practices, consistency
from wemake_python_styleguide.visitors import base, decorators

#: Items that can be inside a hash.
_HashItems = Sequence[Optional[ast.AST]]


@final
@decorators.alias('visit_any_string', (
    'visit_Str',
    'visit_Bytes',
))
class WrongStringVisitor(base.BaseNodeVisitor):
    """Restricts several string usages."""

    _string_constants: ClassVar[FrozenSet[str]] = frozenset((
        string.ascii_letters,
        string.ascii_lowercase,
        string.ascii_uppercase,

        string.digits,
        string.octdigits,
        string.hexdigits,

        string.printable,
        string.whitespace,
        string.punctuation,
    ))

    #: Copied from https://stackoverflow.com/a/30018957/4842742
    _modulo_string_pattern: ClassVar[Pattern] = re.compile(
        r"""                             # noqa: WPS323
        (                                # start of capture group 1
            %                            # literal "%"
            (?:                          # first option
                (?:\([a-zA-Z][\w_]*\))?  # optional named group
                (?:[#0+-]{0,5})          # optional flags (except " ")
                (?:\d+|\*)?              # width
                (?:\.(?:\d+|\*))?        # precision
                (?:h|l|L)?               # size
                [diouxXeEfFgGcrsa]       # type
            ) | %%                       # OR literal "%%"
        )                                # end
        """,                             # noqa: WPS323
        # Different python versions report `WPS323` on different lines.
        flags=re.X,  # flag to ignore comments and whitespaces.
    )

    def visit_any_string(self, node: AnyText) -> None:
        """
        Forbids incorrect usage of strings.

        Raises:
            StringConstantRedefinedViolation
            ModuloStringFormatViolation

        """
        text_data = source.render_string(node.s)
        self._check_is_alphatbet(node, text_data)
        self._check_modulo_patterns(node, text_data)
        self.generic_visit(node)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        """
        Forbids to use ``f`` strings.

        Raises:
            FormattedStringViolation

        """
        self.add_violation(consistency.FormattedStringViolation(node))
        self.generic_visit(node)

    def _check_is_alphatbet(
        self,
        node: AnyText,
        text_data: Optional[str],
    ) -> None:
        if text_data in self._string_constants:
            self.add_violation(
                best_practices.StringConstantRedefinedViolation(
                    node, text=text_data,
                ),
            )

    def _check_modulo_patterns(
        self,
        node: AnyText,
        text_data: Optional[str],
    ) -> None:
        parent = nodes.get_parent(node)
        if parent and strings.is_doc_string(parent):
            return  # we allow `%s` in docstrings: they cannot be formatted.

        if self._modulo_string_pattern.search(text_data):
            self.add_violation(consistency.ModuloStringFormatViolation(node))


@final
class WrongNumberVisitor(base.BaseNodeVisitor):
    """Checks wrong numbers used in the code."""

    _allowed_parents: ClassVar[AnyNodes] = (
        *AssignNodesWithWalrus,

        # Constructor usages:
        *FunctionNodes,
        ast.arguments,

        # Primitives:
        ast.List,
        ast.Dict,
        ast.Set,
        ast.Tuple,
    )

    _non_magic_modulo: ClassVar[int] = 10

    def visit_Num(self, node: ast.Num) -> None:
        """
        Checks wrong constants inside the code.

        Raises:
            MagicNumberViolation
            ApproximateConstantViolation

        """
        self._check_is_magic(node)
        self._check_is_approximate_constant(node)
        self.generic_visit(node)

    def _check_is_magic(self, node: ast.Num) -> None:
        parent = operators.get_parent_ignoring_unary(node)
        if isinstance(parent, self._allowed_parents):
            return

        if node.n in constants.MAGIC_NUMBERS_WHITELIST:
            return

        if isinstance(node.n, int) and node.n <= self._non_magic_modulo:
            return

        self.add_violation(
            best_practices.MagicNumberViolation(node, text=str(node.n)),
        )

    def _check_is_approximate_constant(self, node: ast.Num) -> None:
        try:
            precision = len(str(node.n).split('.')[1])
        except IndexError:
            precision = 0

        if precision < 2:
            return

        for constant in constants.MATH_APPROXIMATE_CONSTANTS:
            if str(constant).startswith(str(node.n)):
                self.add_violation(
                    best_practices.ApproximateConstantViolation(
                        node, text=str(node.n),
                    ),
                )


@final
@decorators.alias('visit_any_for', (
    'visit_For',
    'visit_AsyncFor',
))
@decorators.alias('visit_any_with', (
    'visit_With',
    'visit_AsyncWith',
))
class WrongAssignmentVisitor(base.BaseNodeVisitor):
    """Visits all assign nodes."""

    def visit_any_with(self, node: AnyWith) -> None:
        """
        Checks assignments inside context managers to be correct.

        Raises:
            WrongUnpackingViolation

        """
        for withitem in node.items:
            if isinstance(withitem.optional_vars, ast.Tuple):
                self._check_unpacking_targets(
                    node, withitem.optional_vars.elts,
                )
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Checks comprehensions for the correct assignments.

        Raises:
            WrongUnpackingViolation

        """
        if isinstance(node.target, ast.Tuple):
            self._check_unpacking_targets(node.target, node.target.elts)
        self.generic_visit(node)

    def visit_any_for(self, node: AnyFor) -> None:
        """
        Checks assignments inside ``for`` loops to be correct.

        Raises:
            WrongUnpackingViolation

        """
        if isinstance(node.target, ast.Tuple):
            self._check_unpacking_targets(node, node.target.elts)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Checks assignments to be correct.

        We do not check ``AnnAssign`` here,
        because it does not have problems that we check.

        Raises:
            MultipleAssignmentsViolation
            WrongUnpackingViolation

        """
        self._check_assign_targets(node)
        if isinstance(node.targets[0], ast.Tuple):
            self._check_unpacking_targets(node, node.targets[0].elts)
        self.generic_visit(node)

    def _check_assign_targets(self, node: ast.Assign) -> None:
        if len(node.targets) > 1:
            self.add_violation(
                best_practices.MultipleAssignmentsViolation(node),
            )

    def _check_unpacking_targets(
        self,
        node: ast.AST,
        targets: Iterable[ast.AST],
    ) -> None:
        for target in targets:
            target_name = extract_name(target)
            if target_name is None:  # it means, that non name node was used
                self.add_violation(
                    best_practices.WrongUnpackingViolation(node),
                )


@final
class WrongCollectionVisitor(base.BaseNodeVisitor):
    """Ensures that collection definitions are correct."""

    _elements_in_sets: ClassVar[AnyNodes] = (
        *TextNodes,
        ast.Num,
        ast.NameConstant,
        ast.Name,
    )

    _unhashable_types: ClassVar[AnyNodes] = (
        ast.List,
        ast.ListComp,
        ast.Set,
        ast.SetComp,
        ast.Dict,
        ast.DictComp,
        ast.GeneratorExp,
    )

    _elements_to_eval: ClassVar[AnyNodes] = (
        *TextNodes,
        ast.Num,
        ast.NameConstant,
        ast.Tuple,
        ast.List,
        ast.Set,
        ast.Dict,
        # Since python3.8 `BinOp` only works for complex numbers:
        # https://github.com/python/cpython/pull/4035/files
        # https://bugs.python.org/issue31778
        ast.BinOp,
        # Only our custom `eval` function can eval names safely:
        ast.Name,
    )

    def visit_Set(self, node: ast.Set) -> None:
        """
        Ensures that set literals do not have any duplicate items.

        Raises:
            NonUniqueItemsInHashViolation
            UnhashableTypeInHashViolation

        """
        self._check_set_elements(node, node.elts)
        self._check_unhashable_elements(node.elts)
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        """
        Ensures that dict literals do not have any duplicate keys.

        Raises:
            NonUniqueItemsInHashViolation
            UnhashableTypeInHashViolation
            FloatKeyViolation

        """
        self._check_set_elements(node, node.keys)
        self._check_unhashable_elements(node.keys)
        self._check_float_keys(node.keys)
        self.generic_visit(node)

    def _check_float_keys(self, keys: _HashItems) -> None:
        for dict_key in keys:
            if dict_key is None:
                continue

            real_key = operators.unwrap_unary_node(dict_key)
            is_float_key = (
                isinstance(real_key, ast.Num) and
                isinstance(real_key.n, float)
            )
            if is_float_key:
                self.add_violation(best_practices.FloatKeyViolation(dict_key))

    def _check_unhashable_elements(
        self,
        keys_or_elts: _HashItems,
    ) -> None:
        for set_item in keys_or_elts:
            if isinstance(set_item, self._unhashable_types):
                self.add_violation(
                    best_practices.UnhashableTypeInHashViolation(set_item),
                )

    def _check_set_elements(
        self,
        node: Union[ast.Set, ast.Dict],
        keys_or_elts: _HashItems,
    ) -> None:
        elements: List[str] = []
        element_values = []

        for set_item in keys_or_elts:
            if set_item is None:
                continue   # happens for `{**a}`

            real_item = operators.unwrap_unary_node(set_item)
            if isinstance(real_item, self._elements_in_sets):
                # Similar look:
                node_repr = source.node_to_string(set_item)
                elements.append(node_repr.strip().strip('(').strip(')'))

            real_item = operators.unwrap_starred_node(real_item)

            # Non-constant nodes raise ValueError,
            # unhashables raise TypeError:
            with suppress(ValueError, TypeError):
                # Similar value:
                element_values.append(
                    safe_eval.literal_eval_with_names(
                        real_item,
                    ) if isinstance(
                        real_item, self._elements_to_eval,
                    ) else set_item,
                )
        self._report_set_elements(node, elements, element_values)

    def _report_set_elements(
        self,
        node: Union[ast.Set, ast.Dict],
        elements: List[str],
        element_values,
    ) -> None:
        for look_element, look_count in Counter(elements).items():
            if look_count > 1:
                self.add_violation(
                    best_practices.NonUniqueItemsInHashViolation(
                        node, text=look_element,
                    ),
                )
                return

        value_counts: DefaultDict[Hashable, int] = defaultdict(int)
        for value_element in element_values:
            real_value = value_element if isinstance(
                # Lists, sets, and dicts are not hashable:
                value_element, Hashable,
            ) else str(value_element)

            value_counts[real_value] += 1

            if value_counts[real_value] > 1:
                self.add_violation(
                    best_practices.NonUniqueItemsInHashViolation(
                        node, text=value_element,
                    ),
                )
