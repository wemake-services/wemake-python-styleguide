# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from contextlib import suppress
from typing import ClassVar, Dict, List, Tuple, Type, Union

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.logic.exceptions import get_exception_name
from wemake_python_styleguide.logic.nodes import get_context, get_parent
from wemake_python_styleguide.logic.variables import (
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
    InconsistentReturnVariableViolation,
    InconsistentReturnViolation,
    InconsistentYieldViolation,
    MultipleContextManagerAssignmentsViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

NamesAndReturns = Tuple[
    Dict[str, List[ast.Name]],
    Dict[str, ast.Return],
]
ReturningViolations = Union[
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

        returns = len(list(filter(
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
        violation: ReturningViolations,
    ):
        returns: List[ast.Return] = []
        has_values = False
        for sub_node in ast.walk(node):
            if isinstance(sub_node, returning_type):
                if sub_node.value:
                    has_values = True
                returns.append(sub_node)

        for return_node in returns:
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
@alias('visit_return_variable', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class ConsistentReturningVariableVisitor(BaseNodeVisitor):
    """Finds variables that are only used in `return` statements."""

    _checking_nodes: ClassVar[AnyNodes] = (
        ast.Assign,
        ast.AnnAssign,
        ast.AugAssign,
        ast.Return,
        ast.Name,
    )

    def visit_return_variable(self, node: AnyFunctionDef) -> None:
        """
        Helper to get all ``return`` variables in a function at once.

        Raises:
            InconsistentReturnVariableViolation

        """
        self._check_variables_for_return(node)
        self.generic_visit(node)

    def _get_assign_node_variables(self, node: List[ast.AST]) -> List[str]:
        assign = []
        for sub_node in node:
            if isinstance(sub_node, ast.Assign):
                if isinstance(sub_node.targets[0], ast.Name):
                    assign.append(sub_node.targets[0].id)
            if isinstance(sub_node, ast.AnnAssign):
                if isinstance(sub_node.target, ast.Name):
                    assign.append(sub_node.target.id)
        return assign

    def _get_name_nodes_variable(
        self,
        node: List[ast.AST],
    ) -> Dict[str, List[ast.Name]]:
        names: Dict[str, List[ast.Name]] = defaultdict(list)
        for sub_node in node:
            if isinstance(sub_node, ast.Name):
                if isinstance(sub_node.ctx, ast.Load):
                    names[sub_node.id].append(sub_node)
            if isinstance(sub_node, ast.AugAssign):
                if isinstance(sub_node.target, ast.Name):
                    variable_name = sub_node.target.id
                    names[variable_name].append(sub_node.target)
        return names

    def _get_return_node_variables(
        self,
        node: List[ast.AST],
    ) -> NamesAndReturns:
        returns: Dict[str, List[ast.Name]] = defaultdict(list)
        return_sub_nodes: Dict[str, ast.Return] = defaultdict()
        for sub_node in node:
            if isinstance(sub_node, ast.Return):
                if isinstance(sub_node.value, ast.Name):
                    variable_name = sub_node.value.id
                    returns[variable_name].append(sub_node.value)
                    return_sub_nodes[variable_name] = sub_node
        return returns, return_sub_nodes

    def _is_correct_return_node(
        self,
        node: AnyFunctionDef,
        sub_node: ast.AST,
    ) -> bool:
        if get_context(sub_node) != node:
            return False
        return isinstance(sub_node, self._checking_nodes)

    def _check_variables_for_return(self, node: AnyFunctionDef) -> None:
        nodes = list(
            filter(
                lambda sub: self._is_correct_return_node(node, sub),
                ast.walk(node),
            ),
        )
        assign = self._get_assign_node_variables(nodes)
        names = self._get_name_nodes_variable(nodes)
        returns, return_sub_nodes = self._get_return_node_variables(nodes)

        returns = {name: returns[name] for name in returns if name in assign}

        self._check_for_violations(names, return_sub_nodes, returns)

    def _check_for_violations(self, names, return_sub_nodes, returns) -> None:
        for variable_name in returns:
            if not set(names[variable_name]) - set(returns[variable_name]):
                self.add_violation(
                    InconsistentReturnVariableViolation(
                        return_sub_nodes[variable_name],
                    ),
                )


@final
class ConstantKeywordVisitor(BaseNodeVisitor):
    """Visits keyword definitions to detect contant conditions."""

    def visit_While(self, node: ast.While) -> None:
        """
        Visits ``while`` keyword and tests that loop will execute.

        Raises:
            WrongKeywordConditionViolation

        """
        self._check_condition(node.test)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """
        Visits ``assert`` keyword and tests that condition is correct.

        Raises:
            WrongKeywordConditionViolation

        """
        self._check_condition(node.test)
        self.generic_visit(node)

    def _check_condition(self, condition: ast.AST) -> None:
        with suppress(ValueError):
            constant = ast.literal_eval(condition)
            if not bool(constant):
                self.add_violation(
                    WrongKeywordConditionViolation(
                        condition,
                        text=str(constant) if constant != '' else '""',
                    ),
                )
