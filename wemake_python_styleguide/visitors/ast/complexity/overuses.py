import ast
from collections import defaultdict
from collections.abc import Callable
from typing import ClassVar, TypeAlias, TypeVar, final

from wemake_python_styleguide.compat import nodes
from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic import source, walk
from wemake_python_styleguide.logic.complexity import overuses
from wemake_python_styleguide.logic.tree import annotations
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors import base

#: We use these types to store the number of nodes usage in different contexts.
_Expressions: TypeAlias = defaultdict[str, list[ast.AST]]
_FunctionExpressions: TypeAlias = defaultdict[ast.AST, _Expressions]
_StrOrBytes = TypeVar('_StrOrBytes', str, bytes)


@final
class StringOveruseVisitor(base.BaseNodeVisitor):
    """
    Restricts repeated usage of the same string constant.

    NB: Some short strings are ignored, as their use is very common and
    forcing assignment would not make much sense (i.e. newlines, "",
    comma, dot).
    """

    _ignored_string_constants: ClassVar[frozenset[str]] = frozenset(
        (
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
            '/',
            '...',
        ),
    )
    _ignored_bytes_constants: ClassVar[frozenset[bytes]] = frozenset(
        (
            b'"',
            b"'",
            b'/',
            b' ',
            b'.',
            b',',
            b'',
            b'\n',
            b'\r\n',
            b'\t',
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        """Inits the counter for constants."""
        super().__init__(*args, **kwargs)
        self._string_constants: defaultdict[str, int] = defaultdict(int)
        self._bytes_constants: defaultdict[bytes, int] = defaultdict(int)

        self._string_constants_first_node: defaultdict[
            str,
            ast.Constant,
        ] = defaultdict(lambda: ast.Constant(value=None))
        self._bytes_constants_first_node: defaultdict[
            bytes,
            ast.Constant,
        ] = defaultdict(lambda: ast.Constant(value=None))

    def visit_Str(self, node: ast.Constant) -> None:
        """Restricts to over-use string constants."""
        self._check_constant(
            node,
            str,
            self._ignored_string_constants,
            self._string_constants,
            self._string_constants_first_node,
        )
        self.generic_visit(node)

    def visit_Bytes(self, node: ast.Constant) -> None:
        """Restricts to over-use bytes constants."""
        self._check_constant(
            node,
            bytes,
            self._ignored_bytes_constants,
            self._bytes_constants,
            self._bytes_constants_first_node,
        )
        self.generic_visit(node)

    def _check_constant(
        self,
        node: ast.Constant,
        typechk: type[_StrOrBytes],
        ignored_constants: frozenset[_StrOrBytes],
        constants: defaultdict[_StrOrBytes, int],
        first_nodes: defaultdict[_StrOrBytes, ast.Constant],
    ) -> None:
        if annotations.is_annotation(node):
            return

        # Part of the f-string or t-string:
        if walk.get_closest_parent(
            node,
            parents=(ast.JoinedStr, nodes.TemplateStr),
        ):
            return

        # Some strings are so common, that it makes no sense to check if
        # they are overused.
        if (
            not isinstance(node.value, typechk)
            or node.value in ignored_constants
        ):
            return

        if node.value not in first_nodes:
            first_nodes[node.value] = node

        constants[node.value] += 1

    def _post_visit(self) -> None:
        self._post_visit_violations(
            self._string_constants,
            self._string_constants_first_node,
        )
        self._post_visit_violations(
            self._bytes_constants,
            self._bytes_constants_first_node,
        )

    def _post_visit_violations(
        self,
        constants: defaultdict[_StrOrBytes, int],
        first_nodes: defaultdict[_StrOrBytes, ast.Constant],
    ) -> None:
        for string, usage_count in constants.items():
            if usage_count > self.options.max_string_usages:
                string_value = source.render_string(string)
                self.add_violation(
                    complexity.OverusedStringViolation(
                        text=f'{string_value!r} {usage_count}',
                        baseline=self.options.max_string_usages,
                        node=first_nodes[string],
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

    _ignore_predicates: tuple[Callable[[ast.AST], bool], ...] = (
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
