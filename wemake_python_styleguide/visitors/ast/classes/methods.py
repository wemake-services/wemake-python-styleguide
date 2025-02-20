import ast
from typing import ClassVar, final

from wemake_python_styleguide import constants, types
from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.logic import nodes, walk
from wemake_python_styleguide.logic.arguments import function_args, super_args
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.logic.tree import (
    functions,
    strings,
)
from wemake_python_styleguide.violations import consistency, oop
from wemake_python_styleguide.visitors import base, decorators


@final
@decorators.alias(
    'visit_any_function',
    (
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
    ),
)
class WrongMethodVisitor(base.BaseNodeVisitor):
    """Visits functions, but treats them as methods."""

    _special_async_iter: ClassVar[frozenset[str]] = frozenset(('__aiter__',))

    def visit_any_function(self, node: types.AnyFunctionDef) -> None:
        """Checking class methods: async and regular."""
        node_context = nodes.get_context(node)
        if isinstance(node_context, ast.ClassDef):
            self._check_bound_methods(node)
            self._check_yield_magic_methods(node)
            self._check_async_magic_methods(node)
            self._check_useless_overwritten_methods(
                node,
                class_name=node_context.name,
            )
        self.generic_visit(node)

    def _check_bound_methods(self, node: types.AnyFunctionDef) -> None:
        if functions.is_staticmethod(node):
            self.add_violation(oop.StaticMethodViolation(node))
        elif not functions.get_all_arguments(node):
            self.add_violation(
                oop.MethodWithoutArgumentsViolation(node, text=node.name),
            )

        if node.name in constants.MAGIC_METHODS_BLACKLIST:
            self.add_violation(
                oop.BadMagicMethodViolation(node, text=node.name),
            )

    def _check_yield_magic_methods(self, node: types.AnyFunctionDef) -> None:
        if isinstance(node, ast.AsyncFunctionDef):
            return

        if (
            node.name in constants.YIELD_MAGIC_METHODS_BLACKLIST
            and walk.is_contained(node, (ast.Yield, ast.YieldFrom))
        ):
            self.add_violation(
                oop.YieldMagicMethodViolation(node, text=node.name),
            )

    def _check_async_magic_methods(self, node: types.AnyFunctionDef) -> None:
        if not isinstance(node, ast.AsyncFunctionDef):
            return

        if node.name in self._special_async_iter:
            if not walk.is_contained(node, ast.Yield):  # YieldFrom not async
                self.add_violation(
                    oop.AsyncMagicMethodViolation(node, text=node.name),
                )
        elif node.name in constants.ASYNC_MAGIC_METHODS_BLACKLIST:
            self.add_violation(
                oop.AsyncMagicMethodViolation(node, text=node.name),
            )

    def _check_useless_overwritten_methods(
        self,
        node: types.AnyFunctionDef,
        class_name: str,
    ) -> None:
        if node.decorator_list:
            # Any decorator can change logic and make this overwrite useful.
            return

        if node.args.defaults or list(filter(None, node.args.kw_defaults)):
            # It means that function / method has defaults in args,
            # we cannot be sure that these defaults are the same
            # as in the call def, ignoring it.
            return

        call_stmt = self._get_call_stmt_of_useless_method(node)
        if call_stmt is None or not isinstance(call_stmt.func, ast.Attribute):
            return

        attribute = call_stmt.func
        defined_method_name = node.name
        if defined_method_name != attribute.attr:
            return

        if not super_args.is_ordinary_super_call(
            attribute.value, class_name
        ) or not function_args.is_call_matched_by_arguments(node, call_stmt):
            return

        self.add_violation(
            oop.UselessOverwrittenMethodViolation(
                node,
                text=defined_method_name,
            ),
        )

    def _get_call_stmt_of_useless_method(
        self,
        node: types.AnyFunctionDef,
    ) -> ast.Call | None:
        """
        Fetches ``super`` call statement from function definition.

        Consider next body as possible candidate of useless method:

        1. Optional[docstring]
        2. single return statement with call
        3. single statement with call, but without return

        Related:
        https://github.com/wemake-services/wemake-python-styleguide/issues/1168

        """
        statements_number = len(node.body)
        if statements_number > 2 or statements_number == 0:
            return None

        if statements_number == 2 and not strings.is_doc_string(node.body[0]):
            return None

        stmt = node.body[-1]
        if isinstance(stmt, ast.Return):
            call_stmt = stmt.value
            return call_stmt if isinstance(call_stmt, ast.Call) else None
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            return stmt.value
        return None


@final
class ClassMethodOrderVisitor(base.BaseNodeVisitor):
    """Checks that all methods inside the class are ordered correctly."""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Ensures that class has correct methods order."""
        self._check_method_order(node)
        self.generic_visit(node)

    def _check_method_order(self, node: ast.ClassDef) -> None:
        method_nodes = [
            subnode.name
            for subnode in ast.walk(node)
            if (
                isinstance(subnode, FunctionNodes)
                and nodes.get_context(subnode) is node
            )
        ]

        ideal = sorted(method_nodes, key=self._ideal_order, reverse=True)
        for existing_order, ideal_order in zip(
            method_nodes,
            ideal,
            strict=False,
        ):
            if existing_order != ideal_order:
                self.add_violation(consistency.WrongMethodOrderViolation(node))
                return

    def _ideal_order(self, first: str) -> int:
        base_methods_order = {
            '__init_subclass__': 7,  # highest priority
            '__new__': 6,
            '__init__': 5,
            '__call__': 4,
            '__await__': 3,
        }
        public_and_magic_methods_priority = 2

        if access.is_protected(first):
            return 1
        if access.is_private(first):
            return 0  # lowest priority
        return base_methods_order.get(first, public_and_magic_methods_priority)


@final
class BuggySuperCallVisitor(base.BaseNodeVisitor):
    """
    Responsible for finding wrong form of `super()` call for certain contexts.

    Call to `super()` without arguments will cause unexpected `TypeError` in a
    number of specific contexts. Read more: https://bugs.python.org/issue46175
    """

    _buggy_super_contexts: ClassVar[types.AnyNodes] = (
        ast.GeneratorExp,
        ast.SetComp,
        ast.ListComp,
        ast.DictComp,
    )

    def visit_Call(self, node: ast.Call) -> None:
        """Checks if this is a `super()` call in a specific context."""
        self._check_buggy_super_context(node)
        self.generic_visit(node)

    def _check_buggy_super_context(self, node: ast.Call):
        if not isinstance(node.func, ast.Name):
            return

        if node.func.id != 'super' or node.args:
            return

        # Check for being in a nested function
        ctx = nodes.get_context(node)
        if isinstance(ctx, FunctionNodes):
            outer_ctx = nodes.get_context(ctx)
            if isinstance(outer_ctx, FunctionNodes):
                self.add_violation(oop.BuggySuperContextViolation(node))
                return

        if walk.get_closest_parent(node, self._buggy_super_contexts):
            self.add_violation(oop.BuggySuperContextViolation(node))
