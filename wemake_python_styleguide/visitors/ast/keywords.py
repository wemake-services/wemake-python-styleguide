import ast
from typing import ClassVar, Dict, List, Optional, Type, Union, cast

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import (
    AssignNodes,
    FunctionNodes,
    TextNodes,
)
from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.logic.naming import name_nodes
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.tree import keywords, operators
from wemake_python_styleguide.logic.tree.exceptions import get_exception_name
from wemake_python_styleguide.logic.tree.variables import (
    is_valid_block_variable_definition,
)
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes, AnyWith
from wemake_python_styleguide.violations.best_practices import (
    ContextManagerVariableDefinitionViolation,
    RaiseNotImplementedViolation,
    WrongKeywordConditionViolation,
    WrongKeywordViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ConsecutiveYieldsViolation,
    InconsistentReturnVariableViolation,
    InconsistentReturnViolation,
    InconsistentYieldViolation,
    IncorrectYieldFromTargetViolation,
    MultipleContextManagerAssignmentsViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

#: Utility type to work with violations easier.
_ReturningViolations = Union[
    Type[InconsistentReturnViolation],
    Type[InconsistentYieldViolation],
]


@final
class WrongRaiseVisitor(BaseNodeVisitor):
    """Finds wrong ``raise`` keywords."""

    def visit_Raise(self, node: ast.Raise) -> None:
        """
        Checks how ``raise`` keyword is used.

        Raises:
            RaiseNotImplementedViolation

        """
        self._check_exception_type(node)
        self.generic_visit(node)

    def _check_exception_type(self, node: ast.Raise) -> None:
        exception_name = get_exception_name(node)
        if exception_name == 'NotImplemented':
            self.add_violation(RaiseNotImplementedViolation(node))


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class ConsistentReturningVisitor(BaseNodeVisitor):
    """Finds incorrect and inconsistent ``return`` and ``yield`` nodes."""

    def visit_Return(self, node: ast.Return) -> None:
        """
        Checks ``return`` statements for consistency.

        Raises:
            InconsistentReturnViolation

        """
        self._check_last_return_in_function(node)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Helper to get all ``return`` and ``yield`` nodes in a function at once.

        Raises:
            InconsistentReturnViolation
            InconsistentYieldViolation

        """
        self._check_return_values(node)
        self._check_yield_values(node)
        self.generic_visit(node)

    def _check_last_return_in_function(self, node: ast.Return) -> None:
        parent = get_parent(node)
        if not isinstance(parent, FunctionNodes):
            return

        returns = len(tuple(filter(
            lambda return_node: return_node.value is not None,
            walk.get_subnodes_by_type(parent, ast.Return),
        )))

        last_value_return = (
            len(parent.body) > 1 and
            returns < 2 and
            isinstance(node.value, ast.NameConstant) and
            node.value.value is None
        )
        if node.value is None or last_value_return:
            self.add_violation(InconsistentReturnViolation(node))

    def _iterate_returning_values(
        self,
        node: AnyFunctionDef,
        returning_type,  # mypy is not ok with this type declaration
        violation: _ReturningViolations,
    ):
        return_nodes, has_values = keywords.returning_nodes(
            node, returning_type,
        )

        for return_node in return_nodes:
            if not return_node.value and has_values:
                self.add_violation(violation(return_node))

    def _check_return_values(self, node: AnyFunctionDef) -> None:
        self._iterate_returning_values(
            node, ast.Return, InconsistentReturnViolation,
        )

    def _check_yield_values(self, node: AnyFunctionDef) -> None:
        self._iterate_returning_values(
            node, ast.Yield, InconsistentYieldViolation,
        )


@final
class WrongKeywordVisitor(BaseNodeVisitor):
    """Finds wrong keywords."""

    _forbidden_keywords: ClassVar[AnyNodes] = (
        ast.Pass,
        ast.Delete,
        ast.Global,
        ast.Nonlocal,
    )

    def visit(self, node: ast.AST) -> None:
        """
        Used to find wrong keywords.

        Raises:
            WrongKeywordViolation

        """
        self._check_keyword(node)
        self.generic_visit(node)

    def _check_keyword(self, node: ast.AST) -> None:
        if isinstance(node, self._forbidden_keywords):
            if isinstance(node, ast.Delete):
                message = 'del'
            else:
                message = node.__class__.__qualname__.lower()

            self.add_violation(WrongKeywordViolation(node, text=message))


@final
@alias('visit_any_with', (
    'visit_With',
    'visit_AsyncWith',
))
class WrongContextManagerVisitor(BaseNodeVisitor):
    """Checks context managers."""

    def visit_withitem(self, node: ast.withitem) -> None:
        """
        Checks that all variables inside context managers defined correctly.

        Raises:
            ContextManagerVariableDefinitionViolation

        """
        self._check_variable_definitions(node)
        self.generic_visit(node)

    def visit_any_with(self, node: AnyWith) -> None:
        """
        Checks the number of assignments for context managers.

        Raises:
            MultipleContextManagerAssignmentsViolation

        """
        self._check_target_assignment(node)
        self.generic_visit(node)

    def _check_target_assignment(self, node: AnyWith):
        if len(node.items) > 1:
            self.add_violation(
                MultipleContextManagerAssignmentsViolation(node),
            )

    def _check_variable_definitions(self, node: ast.withitem) -> None:
        if node.optional_vars is None:
            return

        if not is_valid_block_variable_definition(node.optional_vars):
            self.add_violation(
                ContextManagerVariableDefinitionViolation(get_parent(node)),
            )


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
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
        self._yield_locations: Dict[int, ast.Expr] = {}

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        We use this visitor method to check for consecutive ``yield`` nodes.

        Raises:
            ConsecutiveYieldsViolation

        """
        self._check_consecutive_yields(node)
        self.generic_visit(node)

    def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
        """
        Visits `yield from` nodes.

        Raises:
            IncorrectYieldFromTargetViolation

        """
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
        if isinstance(node.value, ast.Tuple):
            if not node.value.elts:
                self.add_violation(IncorrectYieldFromTargetViolation(node))

    def _post_visit(self) -> None:
        previous_line: Optional[int] = None
        previous_parent: Optional[ast.AST] = None

        for line, node in self._yield_locations.items():
            parent = get_parent(node)

            if previous_line is not None:
                if line - 1 == previous_line and previous_parent == parent:
                    self.add_violation(ConsecutiveYieldsViolation(node.value))
                    break

            previous_line = line
            previous_parent = parent


@final
class ConsistentReturningVariableVisitor(BaseNodeVisitor):
    """Finds variables that are only used in ``return`` statements."""

    def visit_Return(self, node: ast.Return) -> None:
        """
        Helper to get all ``return`` variables in a function at once.

        Raises:
            InconsistentReturnVariableViolation

        """
        self._check_consistent_variable_return(node)
        self.generic_visit(node)

    def _check_consistent_variable_return(self, node: ast.Return) -> None:
        if not node.value or not self._is_named_return(node):
            return

        previous_node = self._get_previous_stmt(node)
        if not isinstance(previous_node, AssignNodes):
            return

        return_names = name_nodes.get_variables_from_node(node.value)
        previous_names = list(name_nodes.flat_variable_names([previous_node]))
        self._check_for_violations(node, return_names, previous_names)

    def _is_named_return(self, node: ast.Return) -> bool:
        if isinstance(node.value, ast.Name):
            return True
        return (
            isinstance(node.value, ast.Tuple) and
            all(isinstance(elem, ast.Name) for elem in node.value.elts)
        )

    def _get_previous_stmt(self, node: ast.Return) -> Optional[ast.stmt]:
        """
        This method gets the previous node in a block.

        It is kind of strange. Because nodes might have several bodies.
        Like ``try`` or ``for`` or ``if`` nodes.
        ``return`` can also be the only statement there.

        We also use ``cast`` for a reason.
        Because ``return`` always has a parent.
        """
        parent = cast(ast.AST, get_parent(node))
        for part in ('body', 'orelse', 'finalbody'):
            block = getattr(parent, part, [])
            try:
                current_index = block.index(node)
            except ValueError:
                continue

            if current_index > 0:
                return block[current_index - 1]
        return None

    def _check_for_violations(
        self,
        node: ast.Return,
        return_names: List[str],
        previous_names: List[str],
    ) -> None:
        if previous_names == return_names:
            self.add_violation(
                InconsistentReturnVariableViolation(
                    node, text=', '.join(return_names),
                ),
            )


@final
class ConstantKeywordVisitor(BaseNodeVisitor):
    """Visits keyword definitions to detect contant conditions."""

    _forbidden_nodes: ClassVar[AnyNodes] = (
        ast.NameConstant,

        ast.List,
        ast.Tuple,
        ast.Set,
        ast.Dict,

        ast.ListComp,
        ast.GeneratorExp,
        ast.SetComp,
        ast.DictComp,

        *TextNodes,
        ast.Num,

        ast.IfExp,
    )

    def visit_While(self, node: ast.While) -> None:
        """
        Visits ``while`` keyword and tests that loop will execute.

        Raises:
            WrongKeywordConditionViolation

        """
        self._check_condition(node, node.test)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """
        Visits ``assert`` keyword and tests that condition is correct.

        Raises:
            WrongKeywordConditionViolation

        """
        self._check_condition(node, node.test)
        self.generic_visit(node)

    def _check_condition(self, node: ast.AST, condition: ast.AST) -> None:
        real_node = operators.unwrap_unary_node(condition)
        if isinstance(real_node, ast.NameConstant) and real_node.value is True:
            if isinstance(node, ast.While):
                return  # We should allow `while True:`

        if isinstance(real_node, self._forbidden_nodes):
            self.add_violation(WrongKeywordConditionViolation(condition))
