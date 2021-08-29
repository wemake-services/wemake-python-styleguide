import ast
import re
import string
from collections import Counter, defaultdict
from collections.abc import Hashable
from contextlib import suppress
from typing import (
    ClassVar,
    DefaultDict,
    FrozenSet,
    List,
    Optional,
    Sequence,
    Union,
)
from typing.re import Pattern

from typing_extensions import Final, final

from wemake_python_styleguide import constants
from wemake_python_styleguide.compat.aliases import (
    AssignNodesWithWalrus,
    FunctionNodes,
    TextNodes,
)
from wemake_python_styleguide.compat.functions import get_slice_expr
from wemake_python_styleguide.logic import nodes, safe_eval, source, walk
from wemake_python_styleguide.logic.tree import (
    attributes,
    functions,
    operators,
    strings,
    variables,
)
from wemake_python_styleguide.types import (
    AnyChainable,
    AnyFor,
    AnyNodes,
    AnyText,
    AnyWith,
)
from wemake_python_styleguide.violations import (
    best_practices,
    complexity,
    consistency,
)
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
        flags=re.X,  # flag to ignore comments and whitespace.
    )

    #: Names of functions in which we allow strings with modulo patterns.
    _modulo_pattern_exceptions: ClassVar[FrozenSet[str]] = frozenset((
        'strftime',  # For date, time, and datetime.strftime()
        'strptime',  # For date, time, and datetime.strptime()
        'execute',  # For psycopg2's cur.execute()
    ))

    def visit_any_string(self, node: AnyText) -> None:
        """Forbids incorrect usage of strings."""
        text_data = source.render_string(node.s)
        self._check_is_alphabet(node, text_data)
        self._check_modulo_patterns(node, text_data)
        self.generic_visit(node)

    def _check_is_alphabet(
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

    def _is_modulo_pattern_exception(self, parent: Optional[ast.AST]) -> bool:
        """
        Check if string with modulo pattern is in an exceptional situation.

        Basically we have some function names in which we allow strings with
        modulo patterns because they must have them for the functions to work
        properly.
        """
        if parent and isinstance(parent, ast.Call):
            return bool(functions.given_function_called(
                parent,
                self._modulo_pattern_exceptions,
                split_modules=True,
            ))
        return False

    def _check_modulo_patterns(
        self,
        node: AnyText,
        text_data: Optional[str],
    ) -> None:
        parent = nodes.get_parent(node)
        if parent and strings.is_doc_string(parent):
            return  # we allow `%s` in docstrings: they cannot be formatted.

        if self._modulo_string_pattern.search(text_data):
            if not self._is_modulo_pattern_exception(parent):
                self.add_violation(
                    consistency.ModuloStringFormatViolation(node),
                )


@final
class WrongFormatStringVisitor(base.BaseNodeVisitor):
    """Restricts usage of ``f`` strings."""

    _valid_format_index: ClassVar[AnyNodes] = (
        *TextNodes,
        ast.Num,
        ast.Name,
        ast.NameConstant,
    )
    _single_use_types: ClassVar[AnyNodes] = (
        ast.Call,
        ast.Subscript,
    )
    _chainable_types: Final = (
        ast.Call,
        ast.Subscript,
        ast.Attribute,
    )
    _max_chained_items = 3

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        """Forbids use of ``f`` strings and too complex ``f`` strings."""
        if not isinstance(nodes.get_parent(node), ast.FormattedValue):
            # We don't allow `f` strings by default,
            # But, we need this condition to make sure that this
            # is not a part of complex string format like `f"Count={count:,}"`:
            self._check_complex_formatted_string(node)
            self.add_violation(consistency.FormattedStringViolation(node))
        self.generic_visit(node)

    def _check_complex_formatted_string(self, node: ast.JoinedStr) -> None:
        """
        Whitelists all simple uses of f strings.

        Checks if list, dict, function call with no parameters or variable.
        """
        has_formatted_components = any(
            isinstance(comp, ast.FormattedValue)
            for comp in node.values
        )
        if not has_formatted_components:
            self.add_violation(  # If no formatted values
                complexity.TooComplexFormattedStringViolation(node),
            )
            return

        for string_component in node.values:
            if isinstance(string_component, ast.FormattedValue):
                # Test if possible chaining is invalid
                format_value = string_component.value
                if self._is_valid_formatted_value(format_value):
                    continue
                self.add_violation(  # Everything else is too complex:
                    complexity.TooComplexFormattedStringViolation(node),
                )
                break

    def _is_valid_formatted_value(self, format_value: ast.AST) -> bool:
        if isinstance(format_value, self._chainable_types):
            if not self._is_valid_chaining(format_value):
                return False
        return self._is_valid_final_value(format_value)

    def _is_valid_final_value(self, format_value: ast.AST) -> bool:
        # Variable lookup is okay and a single attribute is okay
        if isinstance(format_value, (ast.Name, ast.Attribute)):
            return True
        # Function call with empty arguments is okay
        elif isinstance(format_value, ast.Call) and not format_value.args:
            return True
        # Named lookup, Index lookup & Dict key is okay
        elif isinstance(format_value, ast.Subscript):
            return isinstance(
                get_slice_expr(format_value),
                self._valid_format_index,
            )
        return False

    def _is_valid_chaining(self, format_value: AnyChainable) -> bool:
        chained_parts: List[ast.AST] = list(attributes.parts(format_value))
        if len(chained_parts) <= self._max_chained_items:
            return self._is_valid_chain_structure(chained_parts)
        return False

    def _is_valid_chain_structure(self, chained_parts: List[ast.AST]) -> bool:
        """Helper method for ``_is_valid_chaining``."""
        has_invalid_parts = any(
            not self._is_valid_final_value(part)
            for part in chained_parts
        )
        if has_invalid_parts:
            return False
        if len(chained_parts) == self._max_chained_items:
            # If there are 3 elements, exactly one must be subscript or
            # call. This is because we don't allow name.attr.attr
            return sum(
                isinstance(part, self._single_use_types)
                for part in chained_parts
            ) == 1
        return True  # All chaining with fewer elements is fine!


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
        """Checks wrong constants inside the code."""
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
        """Checks assignments inside context managers to be correct."""
        for withitem in node.items:
            self._check_unpacking_target_types(withitem.optional_vars)
            if isinstance(withitem.optional_vars, ast.Tuple):
                self._check_unpacking_targets(
                    node, withitem.optional_vars.elts,
                )
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """Checks comprehensions for the correct assignments."""
        self._check_unpacking_target_types(node.target)
        if isinstance(node.target, ast.Tuple):
            self._check_unpacking_targets(node.target, node.target.elts)
        self.generic_visit(node)

    def visit_any_for(self, node: AnyFor) -> None:
        """Checks assignments inside ``for`` loops to be correct."""
        self._check_unpacking_target_types(node.target)
        if isinstance(node.target, ast.Tuple):
            self._check_unpacking_targets(node, node.target.elts)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Checks assignments to be correct.

        We do not check ``AnnAssign`` here,
        because it does not have problems that we check.
        """
        self._check_assign_targets(node)

        for target in node.targets:
            self._check_unpacking_target_types(target)

        if isinstance(node.targets[0], (ast.Tuple, ast.List)):
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
        targets: List[ast.expr],
    ) -> None:
        if len(targets) == 1:
            self.add_violation(
                best_practices.SingleElementDestructuringViolation(node),
            )

        for target in targets:
            if not variables.is_valid_unpacking_target(target):
                self.add_violation(
                    best_practices.WrongUnpackingViolation(node),
                )

    def _check_unpacking_target_types(self, node: Optional[ast.AST]) -> None:
        if not node:
            return
        for subnode in walk.get_subnodes_by_type(node, ast.List):
            self.add_violation(
                consistency.UnpackingIterableToListViolation(subnode),
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
        """Ensures that set literals do not have any duplicate items."""
        self._check_set_elements(node, node.elts)
        self._check_unhashable_elements(node.elts)
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        """Ensures that dict literals do not have any duplicate keys."""
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
