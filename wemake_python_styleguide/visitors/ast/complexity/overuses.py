import ast
from collections import defaultdict
from typing import (
    Callable,
    ClassVar,
    DefaultDict,
    FrozenSet,
    List,
    Tuple,
    Union,
)

from typing_extensions import TypeAlias, final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic import source, walk
from wemake_python_styleguide.logic.complexity import overuses
from wemake_python_styleguide.logic.tree import annotations
from wemake_python_styleguide.types import AnyNodes, AnyText, AnyTextPrimitive
from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors import base, decorators

#: We use these types to store the number of nodes usage in different contexts.
_Expressions: TypeAlias = DefaultDict[str, List[ast.AST]]
_FunctionExpressions: TypeAlias = DefaultDict[ast.AST, _Expressions]
_StringConstants: TypeAlias = FrozenSet[Union[str, bytes]]


@final
@decorators.alias('visit_any_string', (
    'visit_Str',
    'visit_Bytes',
))
class StringOveruseVisitor(base.BaseNodeVisitor):
    """
    Restricts repeated usage of the same string constant.

    NB: Some short strings are ignored, as their use is very common and
    forcing assignment would not make much sense (i.e. newlines, "",
    comma, dot).
    """

    _ignored_string_constants: ClassVar[_StringConstants] = frozenset((
        ' ',
        '.',
        ',',
        '',
        '\n',
        '\r\n',
        '\t',
        '|',
        '"',
        "'",
        b'"',
        b"'",
        b' ',
        b'.',
        b',',
        b'',
        b'\n',
        b'\r\n',
        b'\t',
    ))

    def __init__(self, *args, **kwargs) -> None:
        """Inits the counter for constants."""
        super().__init__(*args, **kwargs)
        self._string_constants: DefaultDict[
            AnyTextPrimitive, int,
        ] = defaultdict(int)

    def visit_any_string(self, node: AnyText) -> None:
        """Restricts to over-use string constants."""
        self._check_string_constant(node)
        self.generic_visit(node)

    def _check_string_constant(self, node: AnyText) -> None:
        if annotations.is_annotation(node):
            return

        # Some strings are so common, that it makes no sense to check if
        # they are overused.
        if node.s in self._ignored_string_constants:
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
        ast.UnaryOp,
        ast.Call,
        ast.Compare,
        ast.Subscript,
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
        annotations.is_annotation,
        overuses.is_class_context,
        overuses.is_super_call,
        overuses.is_primitive,
        overuses.is_unary_minus,
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
        """Visits all nodes in a module to find overused values."""
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
