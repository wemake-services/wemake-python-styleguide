# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from typing import ClassVar, DefaultDict, List, Union

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.constants import SPECIAL_ARGUMENT_NAMES_WHITELIST
from wemake_python_styleguide.logic import nodes, source, walk
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors import base

_Expressions = DefaultDict[str, List[ast.AST]]
_FunctionExpressions = DefaultDict[ast.AST, _Expressions]
_Annotated = Union[ast.arg, ast.AnnAssign]

_AnnNodes = (ast.AnnAssign, ast.arg)


@final
class StringOveruseVisitor(base.BaseNodeVisitor):
    """Restricts several string usages."""

    def __init__(self, *args, **kwargs) -> None:
        """Inits the counter for constants."""
        super().__init__(*args, **kwargs)
        self._string_constants: DefaultDict[str, int] = defaultdict(int)

    def visit_Str(self, node: ast.Str) -> None:
        """
        Restricts to over-use string constants.

        Raises:
            OverusedStringViolation

        """
        self._check_string_constant(node)
        self.generic_visit(node)

    def _check_string_constant(self, node: ast.Str) -> None:
        parent = nodes.get_parent(node)
        if isinstance(parent, _AnnNodes) and parent.annotation == node:
            return  # it is argument or variable annotation

        if isinstance(parent, FunctionNodes) and parent.returns == node:
            return  # it is return annotation

        self._string_constants[node.s] += 1

    def _post_visit(self) -> None:
        for string, usage_count in self._string_constants.items():
            if usage_count > self.options.max_string_usages:
                self.add_violation(
                    complexity.OverusedStringViolation(text=string or "''"),
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
        ast.Starred,
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

    _msg: ClassVar[str] = '{0}; used {1} times'

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
        ignore_predicates = [
            self._is_decorator,
            self._is_self_method,
            self._is_annotation,

            # We use this predicate because classes have quite complex
            # DSL to be created: like django-orm, attrs, and dataclasses.
            # And these DSLs are built using attributes and calls.
            _is_class_context,
            _is_super_call,
        ]
        if any(ignore(node) for ignore in ignore_predicates):
            return

        source_code = source.node_to_string(node)
        self._module_expressions[source_code].append(node)

        maybe_function = walk.get_closest_parent(node, FunctionNodes)
        if maybe_function is not None:
            self._function_expressions[maybe_function][source_code].append(
                node,
            )

    def _is_decorator(
        self,
        node: ast.AST,
    ) -> bool:
        parent = walk.get_closest_parent(node, FunctionNodes)
        if isinstance(parent, FunctionNodes) and parent.decorator_list:
            return any(
                node == decorator or walk.is_contained_by(node, decorator)
                for decorator in parent.decorator_list
            )
        return False

    def _is_self_method(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                if node.func.value.id in SPECIAL_ARGUMENT_NAMES_WHITELIST:
                    return True
        return False

    def _is_annotation(self, node: ast.AST) -> bool:
        typed_assign = walk.get_closest_parent(
            node,
            (ast.AnnAssign, ast.arg),
        )

        if isinstance(typed_assign, _AnnNodes) and typed_assign.annotation:
            is_same_node = node == typed_assign.annotation
            is_child_annotation = walk.is_contained_by(
                node, typed_assign.annotation,
            )
            return is_same_node or is_child_annotation
        return False

    def _post_visit(self) -> None:
        for mod_source, module_nodes in self._module_expressions.items():
            if len(module_nodes) > self.options.max_module_expressions:
                self.add_violation(
                    complexity.OverusedExpressionViolation(
                        module_nodes[0],
                        text=self._msg.format(mod_source, len(module_nodes)),
                    ),
                )

        for function_contexts in self._function_expressions.values():
            for src, function_nodes in function_contexts.items():
                if len(function_nodes) > self.options.max_function_expressions:
                    self.add_violation(
                        complexity.OverusedExpressionViolation(
                            function_nodes[0],
                            text=self._msg.format(src, len(function_nodes)),
                        ),
                    )


def _is_class_context(node: ast.AST) -> bool:
    return isinstance(nodes.get_context(node), ast.ClassDef)


def _is_super_call(node: ast.AST) -> bool:
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return node.func.id == 'super'
    return False
