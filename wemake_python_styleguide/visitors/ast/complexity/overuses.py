import ast
from collections import defaultdict
from typing import Callable, ClassVar, DefaultDict, List, Tuple

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic import source, walk
from wemake_python_styleguide.logic.complexity import overuses
from wemake_python_styleguide.types import AnyNodes, AnyText, AnyTextPrimitive
from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors import base, decorators

#: We use these types to store the number of nodes usage in different contexts.
_Expressions = DefaultDict[str, List[ast.AST]]
_FunctionExpressions = DefaultDict[ast.AST, _Expressions]


@final
@decorators.alias('visit_any_string', (
    'visit_Str',
    'visit_Bytes',
))
class StringOveruseVisitor(base.BaseNodeVisitor):
    """Restricts several string usages."""

    def __init__(self, *args, **kwargs) -> None:
        """Inits the counter for constants."""
        super().__init__(*args, **kwargs)
        self._string_constants: DefaultDict[
            AnyTextPrimitive, int,
        ] = defaultdict(int)

    def visit_any_string(self, node: AnyText) -> None:
        """
        Restricts to over-use string constants.

        Raises:
            OverusedStringViolation

        """
        self._check_string_constant(node)
        self.generic_visit(node)

    def _check_string_constant(self, node: AnyText) -> None:
        if overuses.is_annotation(node):
            return

        self._string_constants[node.s] += 1

    def _post_visit(self) -> None:
        for string, usage_count in self._string_constants.items():
            if usage_count > self.options.max_string_usages:
                self.add_violation(
                    complexity.OverusedStringViolation(
                        text=source.render_string(string) or "''",
                        baseline=self.options.max_string_usages,
                    ),
                )


@final
class ExpressionOveruseVisitor(base.BaseNodeVisitor):
    """Finds overused expressions."""

    _expressions: ClassVar[AnyNodes] = (
        # We do not treat `ast.Attribute`s as expressions
        # because they are too widely used. That's a compromise.
        ast.Assert,
        ast.BoolOp,
        ast.BinOp,
        ast.Call,
        ast.Compare,
        ast.Subscript,
        ast.UnaryOp,
        ast.Lambda,

        ast.DictComp,
        ast.Dict,
        ast.List,
        ast.ListComp,
        ast.Tuple,
        ast.GeneratorExp,
        ast.Set,
        ast.SetComp,
    )

    _ignore_predicates: Tuple[Callable[[ast.AST], bool], ...] = (
        overuses.is_decorator,
        overuses.is_self,
        overuses.is_annotation,
        overuses.is_class_context,
        overuses.is_super_call,
        overuses.is_primitive,
    )

    _msg: ClassVar[str] = '{0}; used {1}'

    def __init__(self, *args, **kwargs) -> None:
        """We need to track expression usage in functions and modules."""
        super().__init__(*args, **kwargs)
        self._module_expressions: _Expressions = defaultdict(list)
        self._function_expressions: _FunctionExpressions = defaultdict(
            lambda: defaultdict(list),
        )

    def visit(self, node: ast.AST) -> None:
        """
        Visits all nodes in a module to find overused values.

        Raises:
            OverusedExpressionViolation

        """
        if isinstance(node, self._expressions):
            self._add_expression(node)
        self.generic_visit(node)

    def _add_expression(self, node: ast.AST) -> None:
        if any(ignore(node) for ignore in self._ignore_predicates):
            return

        source_code = source.node_to_string(node)
        self._module_expressions[source_code].append(node)

        maybe_function = walk.get_closest_parent(node, FunctionNodes)
        if maybe_function is not None:
            self._function_expressions[maybe_function][source_code].append(
                node,
            )

    def _post_visit(self) -> None:
        for mod_source, module_nodes in self._module_expressions.items():
            if len(module_nodes) > self.options.max_module_expressions:
                self.add_violation(
                    complexity.OverusedExpressionViolation(
                        module_nodes[0],
                        text=self._msg.format(mod_source, len(module_nodes)),
                        baseline=self.options.max_module_expressions,
                    ),
                )

        for function_contexts in self._function_expressions.values():
            for src, function_nodes in function_contexts.items():
                if len(function_nodes) > self.options.max_function_expressions:
                    self.add_violation(
                        complexity.OverusedExpressionViolation(
                            function_nodes[0],
                            text=self._msg.format(src, len(function_nodes)),
                            baseline=self.options.max_function_expressions,
                        ),
                    )
