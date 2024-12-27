import ast
from typing import ClassVar, TypeAlias, final

from wemake_python_styleguide.compat.aliases import (
    FunctionNodes,
)
from wemake_python_styleguide.logic import walk, walrus
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.tree import keywords, operators
from wemake_python_styleguide.logic.tree.exceptions import (
    get_cause_name,
    get_exception_name,
)
from wemake_python_styleguide.logic.tree.variables import (
    is_valid_block_variable_definition,
)
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    ContextManagerVariableDefinitionViolation,
    RaiseFromItselfViolation,
    WrongKeywordConditionViolation,
    WrongKeywordViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ConsecutiveYieldsViolation,
    InconsistentReturnViolation,
    InconsistentYieldViolation,
    IncorrectYieldFromTargetViolation,
    RaiseSystemExitViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

#: Utility type to work with violations easier.
_ReturningViolations: TypeAlias = (
    type[InconsistentReturnViolation] | type[InconsistentYieldViolation]
)


@final
class WrongRaiseVisitor(BaseNodeVisitor):
    """Finds wrong ``raise`` keywords."""

    _system_error_name: ClassVar[str] = 'SystemExit'

    def visit_Raise(self, node: ast.Raise) -> None:
        """Checks how ``raise`` keyword is used."""
        self._check_raise_from_itself(node)
        self._check_raise_system_error(node)
        self.generic_visit(node)

    def _check_raise_from_itself(self, node: ast.Raise) -> None:
        raising_name = get_exception_name(node)
        names_are_same = raising_name == get_cause_name(node)
        if raising_name is not None and names_are_same:
            self.add_violation(RaiseFromItselfViolation(node))

    def _check_raise_system_error(self, node: ast.Raise) -> None:
        if get_exception_name(node) == self._system_error_name:
            self.add_violation(RaiseSystemExitViolation(node))


@final
@alias(
    'visit_any_function',
    (
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
    ),
)
class ConsistentReturningVisitor(BaseNodeVisitor):
    """Finds incorrect and inconsistent ``return`` and ``yield`` nodes."""

    def visit_Return(self, node: ast.Return) -> None:
        """Checks ``return`` statements for consistency."""
        self._check_last_return_in_function(node)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """All ``return`` and ``yield`` nodes in a function at once."""
        self._check_return_values(node)
        self._check_yield_values(node)
        self.generic_visit(node)

    def _check_last_return_in_function(self, node: ast.Return) -> None:
        parent = get_parent(node)
        if not isinstance(parent, FunctionNodes):
            return

        returns = len(
            tuple(
                filter(
                    lambda return_node: return_node.value is not None,
                    walk.get_subnodes_by_type(parent, ast.Return),
                ),
            ),
        )

        last_value_return = (
            len(parent.body) > 1
            and returns < 2
            and isinstance(node.value, ast.Constant)
            and node.value.value is None
        )

        one_return_with_none = (
            returns == 1
            and isinstance(node.value, ast.Constant)
            and node.value.value is None
        )

        if node.value is None or last_value_return or one_return_with_none:
            self.add_violation(InconsistentReturnViolation(node))

    def _iterate_returning_values(
        self,
        node: AnyFunctionDef,
        returning_type: type[ast.Return] | type[ast.Yield],
        violation: _ReturningViolations,
    ):
        return_nodes, has_values = keywords.returning_nodes(
            node,
            returning_type,
        )
        is_all_none = has_values and all(
            (
                isinstance(ret_node.value, ast.Constant)
                and ret_node.value.value is None
            )
            for ret_node in return_nodes
        )
        if is_all_none:
            self.add_violation(violation(node))

        for return_node in return_nodes:
            if not return_node.value and has_values:
                self.add_violation(violation(return_node))

    def _check_return_values(self, node: AnyFunctionDef) -> None:
        self._iterate_returning_values(
            node,
            ast.Return,
            InconsistentReturnViolation,
        )

    def _check_yield_values(self, node: AnyFunctionDef) -> None:
        self._iterate_returning_values(
            node,
            ast.Yield,
            InconsistentYieldViolation,
        )


@final
@alias(
    'visit_forbidden_keyword',
    (
        'visit_Pass',
        'visit_Delete',
        'visit_Global',
        'visit_Nonlocal',
    ),
)
class WrongKeywordVisitor(BaseNodeVisitor):
    """Finds wrong keywords."""

    def visit_forbidden_keyword(self, node: ast.AST) -> None:
        """Used to find wrong keywords."""
        self._check_keyword(node)
        self.generic_visit(node)

    def _check_keyword(self, node: ast.AST) -> None:
        if isinstance(node, ast.Pass) and walk.get_closest_parent(
            node, ast.match_case
        ):
            return  # We allow `pass` in `match: case:`

        if isinstance(node, ast.Delete):
            message = 'del'
        else:
            message = node.__class__.__qualname__.lower()

        self.add_violation(WrongKeywordViolation(node, text=message))


@final
class WrongContextManagerVisitor(BaseNodeVisitor):
    """Checks context managers."""

    def visit_withitem(self, node: ast.withitem) -> None:
        """Variables inside context managers must be defined correctly."""
        self._check_variable_definitions(node)
        self.generic_visit(node)

    def _check_variable_definitions(self, node: ast.withitem) -> None:
        if node.optional_vars is None:
            return

        if not is_valid_block_variable_definition(node.optional_vars):
            self.add_violation(
                ContextManagerVariableDefinitionViolation(get_parent(node)),
            )


@final
@alias(
    'visit_any_function',
    (
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
    ),
)
class GeneratorKeywordsVisitor(BaseNodeVisitor):
    """Checks how generators are defined and used."""

    _allowed_nodes: ClassVar[AnyNodes] = (
        ast.Name,
        ast.Call,
        ast.Attribute,
        ast.Subscript,
        ast.Tuple,
        ast.GeneratorExp,
    )

    def __init__(self, *args, **kwargs) -> None:
        """Here we store the information about ``yield`` locations."""
        super().__init__(*args, **kwargs)
        self._yield_locations: dict[int, ast.Expr] = {}

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Checks for consecutive ``yield`` nodes."""
        self._check_consecutive_yields(node)
        self.generic_visit(node)

    def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
        """Checks ``yield from`` nodes."""
        self._check_yield_from_type(node)
        self._check_yield_from_empty(node)
        self.generic_visit(node)

    def _check_consecutive_yields(self, node: AnyFunctionDef) -> None:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Expr) and isinstance(sub.value, ast.Yield):
                self._yield_locations[sub.value.lineno] = sub

    def _check_yield_from_type(self, node: ast.YieldFrom) -> None:
        if not isinstance(node.value, self._allowed_nodes):
            self.add_violation(IncorrectYieldFromTargetViolation(node))

    def _check_yield_from_empty(self, node: ast.YieldFrom) -> None:
        if isinstance(node.value, ast.Tuple) and not node.value.elts:
            self.add_violation(IncorrectYieldFromTargetViolation(node))

    def _post_visit(self) -> None:
        previous_line: int | None = None
        previous_parent: ast.AST | None = None

        for line, node in self._yield_locations.items():
            parent = get_parent(node)

            if (
                previous_line is not None
                and line - 1 == previous_line
                and previous_parent == parent
            ):
                self.add_violation(ConsecutiveYieldsViolation(node.value))
                break

            previous_line = line
            previous_parent = parent


@final
class ConstantKeywordVisitor(BaseNodeVisitor):
    """Visits keyword definitions to detect constant conditions."""

    _forbidden_nodes: ClassVar[AnyNodes] = (
        ast.Constant,
        ast.List,
        ast.Tuple,
        ast.Set,
        ast.Dict,
        ast.ListComp,
        ast.GeneratorExp,
        ast.SetComp,
        ast.DictComp,
        ast.Constant,
        ast.IfExp,
    )

    def visit_While(self, node: ast.While) -> None:
        """Visits ``while`` keyword and tests that loop will execute."""
        self._check_condition(node, node.test)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """Visits ``assert`` keyword and tests that condition is correct."""
        self._check_condition(node, node.test)
        self.generic_visit(node)

    def _check_condition(self, node: ast.AST, cond: ast.AST) -> None:
        if (
            isinstance(cond, ast.Constant)
            and cond.value is True
            and isinstance(node, ast.While)
        ):
            return  # We should allow plain `while True:`

        real_node = operators.unwrap_unary_node(walrus.get_assigned_expr(cond))
        if isinstance(real_node, self._forbidden_nodes):
            self.add_violation(WrongKeywordConditionViolation(cond))
