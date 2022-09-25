import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, List, Mapping, Tuple, Type, Union

from typing_extensions import TypeAlias, final

from wemake_python_styleguide.logic.complexity import cognitive
from wemake_python_styleguide.logic.complexity.functions import (
    ComplexityMetrics,
    FunctionCounter,
    FunctionCounterWithLambda,
)
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.tree import functions
from wemake_python_styleguide.types import (
    AnyFunctionDef,
    AnyFunctionDefAndLambda,
    AnyNodes,
)
from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.violations.base import BaseViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

# Type aliases:

_AnyFunctionCounter: TypeAlias = Union[
    FunctionCounter,
    FunctionCounterWithLambda,
]
_CheckRule: TypeAlias = Tuple[_AnyFunctionCounter, int, Type[BaseViolation]]
_NodeTypeHandler: TypeAlias = Mapping[
    Union[type, Tuple[type, ...]],
    FunctionCounter,
]


@final
class _ComplexityCounter(object):
    """Helper class to encapsulate logic from the visitor."""

    _not_contain_locals: ClassVar[AnyNodes] = (
        ast.comprehension,
    )

    def __init__(self) -> None:
        self.metrics = ComplexityMetrics()

    def check_arguments_count(self, node: AnyFunctionDefAndLambda) -> None:
        """Checks the number of the arguments in a function."""
        self.metrics.arguments[node] = len(functions.get_all_arguments(node))

    def check_function_complexity(self, node: AnyFunctionDef) -> None:
        """
        In this function we iterate all the internal body's node.

        We check different complexity metrics based on these internals.
        """
        for body_item in node.body:
            for sub_node in ast.walk(body_item):
                self._check_sub_node(node, sub_node)

    def _update_variables(
        self,
        function: AnyFunctionDef,
        variable_def: ast.Name,
    ) -> None:
        """
        Increases the counter of local variables.

        What is treated as a local variable?
        Check ``TooManyLocalsViolation`` documentation.
        """
        function_variables = self.metrics.variables[function]
        if variable_def.id not in function_variables:
            if access.is_unused(variable_def.id):
                return

            parent = get_parent(variable_def)
            no_locals = self._not_contain_locals
            if isinstance(parent, no_locals):
                return

            function_variables.append(variable_def.id)

    def _check_sub_node(
        self,
        node: AnyFunctionDef,
        sub_node: ast.AST,
    ) -> None:
        if isinstance(sub_node, ast.Name):
            if isinstance(sub_node.ctx, ast.Store):
                self._update_variables(node, sub_node)

        error_counters: _NodeTypeHandler = {
            ast.Return: self.metrics.returns,
            ast.Expr: self.metrics.expressions,
            ast.Await: self.metrics.awaits,
            ast.Assert: self.metrics.asserts,
            ast.Raise: self.metrics.raises,
        }

        for types, counter in error_counters.items():
            if isinstance(sub_node, types):
                counter[node] += 1


@final
@alias('visit_any_function', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class FunctionComplexityVisitor(BaseNodeVisitor):
    """
    This class checks for complexity inside functions.

    This includes:

    1. Number of arguments
    2. Number of `return` statements
    3. Number of expressions
    4. Number of local variables

    """

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked metrics."""
        super().__init__(*args, **kwargs)
        self._counter = _ComplexityCounter()

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Checks function's internal complexity."""
        self._counter.check_arguments_count(node)
        self._counter.check_function_complexity(node)
        self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """Checks lambda function's internal complexity."""
        self._counter.check_arguments_count(node)
        self.generic_visit(node)

    def _check_function_internals(self) -> None:
        for var_node, variables in self._counter.metrics.variables.items():
            if len(variables) > self.options.max_local_variables:
                self.add_violation(
                    complexity.TooManyLocalsViolation(
                        var_node,
                        text=str(len(variables)),
                        baseline=self.options.max_local_variables,
                    ),
                )

        for exp_node, expressions in self._counter.metrics.expressions.items():
            if expressions > self.options.max_expressions:
                self.add_violation(
                    complexity.TooManyExpressionsViolation(
                        exp_node,
                        text=str(expressions),
                        baseline=self.options.max_expressions,
                    ),
                )

    def _check_function_signature(self) -> None:
        for counter, limit, violation in self._function_checks():
            for node, count in counter.items():
                if count > limit:
                    self.add_violation(
                        violation(node, text=str(count), baseline=limit),
                    )

    def _function_checks(self) -> List[_CheckRule]:
        return [
            (
                self._counter.metrics.arguments,
                self.options.max_arguments,
                complexity.TooManyArgumentsViolation,
            ),
            (
                self._counter.metrics.returns,
                self.options.max_returns,
                complexity.TooManyReturnsViolation,
            ),
            (
                self._counter.metrics.awaits,
                self.options.max_awaits,
                complexity.TooManyAwaitsViolation,
            ),
            (
                self._counter.metrics.asserts,
                self.options.max_asserts,
                complexity.TooManyAssertsViolation,
            ),
            (
                self._counter.metrics.raises,
                self.options.max_raises,
                complexity.TooManyRaisesViolation,
            ),
        ]

    def _post_visit(self) -> None:
        self._check_function_signature()
        self._check_function_internals()


@final
@alias('visit_any_function', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class CognitiveComplexityVisitor(BaseNodeVisitor):
    """Used to count cognitive score and average module complexity."""

    def __init__(self, *args, **kwargs) -> None:
        """We use to save all functions' complexity here."""
        super().__init__(*args, **kwargs)
        self._functions: DefaultDict[AnyFunctionDef, int] = defaultdict(int)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Counts cognitive complexity."""
        self._functions[node] = cognitive.cognitive_score(node)
        self.generic_visit(node)

    def _post_visit(self) -> None:
        if not self._functions:
            return  # module can be empty

        total = 0
        for function, score in self._functions.items():
            total += score

            if score > self.options.max_cognitive_score:
                self.add_violation(
                    complexity.CognitiveComplexityViolation(
                        function,
                        text=str(score),
                        baseline=self.options.max_cognitive_score,
                    ),
                )

        if len(self._functions) <= 1:
            return  # We don't check module average for a single function.

        average = total / len(self._functions)
        if average > self.options.max_cognitive_average:
            self.add_violation(
                complexity.CognitiveModuleComplexityViolation(
                    text=str(round(average, 1)),
                    baseline=self.options.max_cognitive_average,
                ),
            )
