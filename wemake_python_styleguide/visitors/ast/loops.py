import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, List, Mapping, Sequence, Type, Union

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import AssignNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic import nodes, source, walk
from wemake_python_styleguide.logic.tree import loops, operators, slices
from wemake_python_styleguide.logic.tree.variables import (
    is_valid_block_variable_definition,
)
from wemake_python_styleguide.types import (
    AnyComprehension,
    AnyFor,
    AnyLoop,
    AnyNodes,
)
from wemake_python_styleguide.violations.best_practices import (
    LambdaInsideLoopViolation,
    LoopVariableDefinitionViolation,
    YieldInComprehensionViolation,
)
from wemake_python_styleguide.violations.complexity import (
    TooManyForsInComprehensionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    MultilineLoopViolation,
    MultipleIfsInComprehensionViolation,
    UselessContinueViolation,
    WrongLoopIterTypeViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    ImplicitItemsIteratorViolation,
    ImplicitSumViolation,
    ImplicitYieldFromViolation,
    UselessLoopElseViolation,
)
from wemake_python_styleguide.visitors import base, decorators

#: Type alias to specify how we check different containers in loops.
_ContainerSpec = Mapping[Type[ast.AST], Sequence[str]]


@final
@decorators.alias('visit_any_comprehension', (
    'visit_ListComp',
    'visit_DictComp',
    'visit_SetComp',
    'visit_GeneratorExp',
))
class WrongComprehensionVisitor(base.BaseNodeVisitor):
    """Checks comprehensions for correctness."""

    _max_ifs: ClassVar[int] = 1
    _max_fors: ClassVar[int] = 2

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._fors: DefaultDict[ast.AST, int] = defaultdict(int)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Finds multiple ``if`` and ``for`` nodes inside the comprehension.

        Raises:
            MultipleIfsInComprehensionViolation
            TooManyForsInComprehensionViolation

        """
        self._check_ifs(node)
        self._check_fors(node)
        self.generic_visit(node)

    def visit_any_comprehension(self, node: AnyComprehension) -> None:
        """
        Finds incorrect patterns inside comprehensions.

        Raises:
            YieldInComprehensionViolation

        """
        self._check_contains_yield(node)
        self.generic_visit(node)

    def _check_ifs(self, node: ast.comprehension) -> None:
        if len(node.ifs) > self._max_ifs:
            # We are trying to fix line number in the report,
            # since `comprehension` does not have this property.
            parent = nodes.get_parent(node) or node
            self.add_violation(MultipleIfsInComprehensionViolation(parent))

    def _check_fors(self, node: ast.comprehension) -> None:
        parent = nodes.get_parent(node)
        self._fors[parent] = len(parent.generators)  # type: ignore

    def _check_contains_yield(self, node: AnyComprehension) -> None:
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Yield):  # pragma: py-gte-38
                self.add_violation(YieldInComprehensionViolation(node))

    def _post_visit(self) -> None:
        for node, for_count in self._fors.items():
            if for_count > self._max_fors:
                self.add_violation(TooManyForsInComprehensionViolation(node))


@final
@decorators.alias('visit_any_loop', (
    'visit_For',
    'visit_While',
    'visit_AsyncFor',
))
@decorators.alias('visit_any_comp', (
    'visit_ListComp',
    'visit_SetComp',
    'visit_DictComp',
    'visit_GeneratorExp',
))
class WrongLoopVisitor(base.BaseNodeVisitor):
    """Responsible for examining loops."""

    _containers: ClassVar[_ContainerSpec] = {
        ast.ListComp: ['elt'],
        ast.SetComp: ['elt'],
        ast.GeneratorExp: ['elt'],
        ast.DictComp: ['key', 'value'],

        ast.For: ['body'],
        ast.AsyncFor: ['body'],
        ast.While: ['body'],
    }

    def visit_any_comp(self, node: AnyComprehension) -> None:
        """
        Checks all kinds of comprehensions.

        Raises:
            LambdaInsideLoopViolation

        """
        self._check_lambda_inside_loop(node)
        self.generic_visit(node)

    def visit_any_loop(self, node: AnyLoop) -> None:
        """
        Checks ``for`` and ``while`` loops.

        Raises:
            UselessLoopElseViolation
            LambdaInsideLoopViolation
            MultilineLoopViolation

        """
        self._check_loop_needs_else(node)
        self._check_lambda_inside_loop(node)
        self._check_useless_continue(node)
        self._check_multiline_loop(node)
        self.generic_visit(node)

    def _check_loop_needs_else(self, node: AnyLoop) -> None:
        if node.orelse and not loops.has_break(node):
            self.add_violation(UselessLoopElseViolation(node))

    def _check_lambda_inside_loop(
        self,
        node: Union[AnyLoop, AnyComprehension],
    ) -> None:
        container_names = self._containers.get(type(node), ())
        for container in container_names:
            body = getattr(node, container, [])
            if not isinstance(body, list):
                body = [body]

            for subnode in body:
                if walk.is_contained(subnode, ast.Lambda):
                    self.add_violation(LambdaInsideLoopViolation(node))

    def _check_useless_continue(self, node: AnyLoop) -> None:
        nodes_at_line: DefaultDict[int, List[ast.AST]] = defaultdict(list)
        for sub_node in ast.walk(node):
            lineno = getattr(sub_node, 'lineno', None)
            if lineno is not None:
                nodes_at_line[lineno].append(sub_node)

        last_line = nodes_at_line[sorted(nodes_at_line.keys())[-1]]
        if any(isinstance(last, ast.Continue) for last in last_line):
            self.add_violation(UselessContinueViolation(node))

    def _check_multiline_loop(self, node: AnyLoop) -> None:
        start_lineno = getattr(node, 'lineno', None)

        if isinstance(node, ast.While):
            node_to_check = node.test
        else:
            node_to_check = node.iter

        for sub_node in ast.walk(node_to_check):
            sub_lineno = getattr(sub_node, 'lineno', None)
            if sub_lineno is not None and sub_lineno > start_lineno:
                self.add_violation(MultilineLoopViolation(node))
                break


@final
@decorators.alias('visit_any_for', (
    'visit_For',
    'visit_AsyncFor',
))
class WrongLoopDefinitionVisitor(base.BaseNodeVisitor):
    """Responsible for ``for`` loops and comprehensions definitions."""

    _forbidden_for_iters: ClassVar[AnyNodes] = (
        ast.List,
        ast.ListComp,
        ast.Dict,
        ast.DictComp,
        ast.Set,
        ast.SetComp,
        ast.GeneratorExp,
        ast.Num,
        ast.NameConstant,
    )

    def visit_any_for(self, node: AnyFor) -> None:
        """
        Ensures that ``for`` loop definitions are correct.

        Raises:
            LoopVariableDefinitionViolation
            WrongLoopIterTypeViolation
            ImplicitSumViolation

        """
        self._check_variable_definitions(node.target)
        self._check_explicit_iter_type(node)
        self._check_implicit_sum(node)
        self._check_implicit_yield_from(node)
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        """
        Ensures that comprehension definitions are correct.

        Raises:
            LoopVariableDefinitionViolation

        """
        self._check_variable_definitions(node.target)
        self._check_explicit_iter_type(node)
        self.generic_visit(node)

    def _check_variable_definitions(self, node: ast.AST) -> None:
        if not is_valid_block_variable_definition(node):
            self.add_violation(LoopVariableDefinitionViolation(node))

    def _check_explicit_iter_type(
        self,
        node: Union[AnyFor, ast.comprehension],
    ) -> None:
        node_iter = operators.unwrap_unary_node(node.iter)
        is_wrong = isinstance(node_iter, self._forbidden_for_iters)
        is_empty = isinstance(node_iter, ast.Tuple) and not node_iter.elts
        if is_wrong or is_empty:
            self.add_violation(WrongLoopIterTypeViolation(node_iter))

    def _check_implicit_sum(self, node: AnyFor) -> None:
        is_implicit_sum = (
            len(node.body) == 1 and
            isinstance(node.body[0], ast.AugAssign) and
            isinstance(node.body[0].op, ast.Add) and
            isinstance(node.body[0].target, ast.Name)
        )
        if is_implicit_sum:
            self.add_violation(ImplicitSumViolation(node))

    def _check_implicit_yield_from(self, node: AnyFor) -> None:
        if isinstance(nodes.get_context(node), ast.AsyncFunctionDef):
            # Python does not support 'yield from' inside async functions
            return

        is_implicit_yield_from = (
            len(node.body) == 1 and
            isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Yield)
        )
        if is_implicit_yield_from:
            self.add_violation(ImplicitYieldFromViolation(node))


@final
class SyncForLoopVisitor(base.BaseNodeVisitor):
    """We use this visitor to check just sync ``for`` loops."""

    def visit_For(self, node: ast.For) -> None:
        """
        Checks for hidden patterns in sync loops.

        Raises:
            ImplicitItemsIteratorViolation

        """
        self._check_implicit_items(node)
        self.generic_visit(node)

    def _check_implicit_items(self, node: ast.For) -> None:
        iterable = source.node_to_string(node.iter)
        target = source.node_to_string(node.target)

        for sub in ast.walk(node):
            has_violation = (
                isinstance(sub, ast.Subscript) and
                not self._is_assigned_target(sub) and
                slices.is_same_slice(iterable, target, sub)
            )
            if has_violation:
                self.add_violation(ImplicitItemsIteratorViolation(node))
                break

    def _is_assigned_target(self, node: ast.Subscript) -> bool:
        parent = nodes.get_parent(node)
        if not isinstance(parent, (*AssignNodes, ast.AugAssign)):
            return False
        return any(node == target for target in get_assign_targets(parent))
