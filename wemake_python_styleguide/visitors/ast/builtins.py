import ast
import string
from collections.abc import Sequence
from typing import ClassVar, Final, TypeAlias

from typing_extensions import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.compat.aliases import (
    AssignNodesWithWalrus,
    FunctionNodes,
    TextNodes,
)
from wemake_python_styleguide.logic import nodes, source, walk
from wemake_python_styleguide.logic.tree import (
    attributes,
    operators,
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
_HashItems: TypeAlias = Sequence[ast.AST | None]


@final
@decorators.alias(
    'visit_any_string',
    (
        'visit_Str',
        'visit_Bytes',
    ),
)
class WrongStringVisitor(base.BaseNodeVisitor):
    """Restricts several string usages."""

    _string_constants: ClassVar[frozenset[str]] = frozenset(
        (
            string.ascii_letters,
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
            string.octdigits,
            string.hexdigits,
            string.printable,
            string.whitespace,
            string.punctuation,
        ),
    )

    def visit_any_string(self, node: AnyText) -> None:
        """Forbids incorrect usage of strings."""
        text_data = source.render_string(node.s)
        self._check_is_alphabet(node, text_data)
        self.generic_visit(node)

    def _check_is_alphabet(
        self,
        node: AnyText,
        text_data: str | None,
    ) -> None:
        if text_data in self._string_constants:
            self.add_violation(
                best_practices.StringConstantRedefinedViolation(
                    node,
                    text=text_data,
                ),
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
            # We need this condition to make sure that this
            # is not a part of complex string format like `f"Count={count:,}"`:
            self._check_complex_formatted_string(node)
        self.generic_visit(node)

    def _check_complex_formatted_string(self, node: ast.JoinedStr) -> None:
        """Allows all simple uses of `f` strings."""
        for string_component in node.values:
            if isinstance(string_component, ast.FormattedValue):
                # Test if possible chaining is invalid
                if self._is_valid_formatted_value(string_component.value):
                    continue
                self.add_violation(  # Everything else is too complex:
                    complexity.TooComplexFormattedStringViolation(node),
                )
                return

    def _is_valid_formatted_value(self, format_value: ast.AST) -> bool:
        if isinstance(
            format_value,
            self._chainable_types,
        ) and not self._is_valid_chaining(format_value):
            return False
        return self._is_valid_final_value(format_value)

    def _is_valid_final_value(self, format_value: ast.AST) -> bool:
        # Variable lookup is okay and a single attribute is okay
        if isinstance(format_value, ast.Name | ast.Attribute) or (
            isinstance(format_value, ast.Call) and len(format_value.args) <= 3
        ):
            return True
        # Named lookup, Index lookup & Dict key is okay
        if isinstance(format_value, ast.Subscript):
            return isinstance(
                format_value.slice,
                self._valid_format_index,
            )
        return False

    def _is_valid_chaining(self, format_value: AnyChainable) -> bool:
        chained_parts: list[ast.AST] = list(attributes.parts(format_value))
        if len(chained_parts) <= self._max_chained_items:
            return self._is_valid_chain_structure(chained_parts)
        return False

    def _is_valid_chain_structure(self, chained_parts: list[ast.AST]) -> bool:
        """Helper method for ``_is_valid_chaining``."""
        has_invalid_parts = any(
            not self._is_valid_final_value(part) for part in chained_parts
        )
        if has_invalid_parts:
            return False
        if len(chained_parts) == self._max_chained_items:
            # If there are 3 elements, exactly one must be subscript or
            # call. This is because we don't allow name.attr.attr
            return (
                sum(
                    isinstance(part, self._single_use_types)
                    for part in chained_parts
                )
                == 1
            )
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
                        node,
                        text=str(node.n),
                    ),
                )


@final
@decorators.alias(
    'visit_any_for',
    (
        'visit_For',
        'visit_AsyncFor',
    ),
)
@decorators.alias(
    'visit_any_with',
    (
        'visit_With',
        'visit_AsyncWith',
    ),
)
class WrongAssignmentVisitor(base.BaseNodeVisitor):
    """Visits all assign nodes."""

    def visit_any_with(self, node: AnyWith) -> None:
        """Checks assignments inside context managers to be correct."""
        for withitem in node.items:
            self._check_unpacking_target_types(withitem.optional_vars)
            if isinstance(withitem.optional_vars, ast.Tuple):
                self._check_unpacking_targets(
                    node,
                    withitem.optional_vars.elts,
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

        if isinstance(node.targets[0], ast.Tuple | ast.List):
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
        targets: list[ast.expr],
    ) -> None:
        if len(targets) == 1:
            self.add_violation(
                best_practices.SingleElementDestructuringViolation(node),
            )
        elif variables.is_getting_element_by_unpacking(targets):
            self.add_violation(
                best_practices.GettingElementByUnpackingViolation(
                    node,
                ),
            )

        for target in targets:
            if not variables.is_valid_unpacking_target(target):
                self.add_violation(
                    best_practices.WrongUnpackingViolation(node),
                )

    def _check_unpacking_target_types(self, node: ast.AST | None) -> None:
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
        self._check_unhashable_elements(node.elts)
        self.generic_visit(node)

    def visit_Dict(self, node: ast.Dict) -> None:
        """Ensures that dict literals do not have any duplicate keys."""
        self._check_unhashable_elements(node.keys)
        self._check_float_keys(node.keys)
        self.generic_visit(node)

    def _check_float_keys(self, keys: _HashItems) -> None:
        for dict_key in keys:
            if dict_key is None:
                continue

            evaluates_to_float = False
            if isinstance(dict_key, ast.BinOp):
                evaluated_key = getattr(dict_key, 'wps_op_eval', None)
                evaluates_to_float = isinstance(evaluated_key, float)

            real_key = operators.unwrap_unary_node(dict_key)
            is_float_key = isinstance(real_key, ast.Num) and isinstance(
                real_key.n,
                float,
            )
            if is_float_key or evaluates_to_float:
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
