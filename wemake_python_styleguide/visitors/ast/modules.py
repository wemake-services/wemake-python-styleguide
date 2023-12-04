import ast
from typing import ClassVar, Iterable, cast

from typing_extensions import final

from wemake_python_styleguide import constants
from wemake_python_styleguide.logic.filenames import get_stem
from wemake_python_styleguide.logic.naming.constants import is_constant
from wemake_python_styleguide.logic.nodes import get_context
from wemake_python_styleguide.logic.tree.strings import is_doc_string
from wemake_python_styleguide.types import AnyAssign, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    BadMagicModuleFunctionViolation,
    EmptyModuleViolation,
    InitModuleHasLogicViolation,
    MutableModuleConstantViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
class EmptyModuleContentsVisitor(BaseNodeVisitor):
    """Restricts to have empty modules."""

    def visit_Module(self, node: ast.Module) -> None:
        """
        Checks that module has something other than module definition.

        We have completely different rules
        for ``__init__.py`` and regular files.
        Since, we believe that ``__init__.py`` must be empty.
        But, other files must have contents.
        """
        self._check_init_contents(node)
        self._check_module_contents(node)
        self.generic_visit(node)

    def _is_init(self) -> bool:
        return get_stem(self.filename) == constants.INIT

    def _check_module_contents(self, node: ast.Module) -> None:
        if self._is_init():
            return
        if not node.body:
            self.add_violation(EmptyModuleViolation())

    def _check_init_contents(self, node: ast.Module) -> None:
        if not self._is_init() or not node.body:
            return

        if not self.options.i_control_code:
            return

        if len(node.body) > 1:
            self.add_violation(InitModuleHasLogicViolation())
            return

        if not is_doc_string(node.body[0]):
            self.add_violation(InitModuleHasLogicViolation())


@final
class MagicModuleFunctionsVisitor(BaseNodeVisitor):
    """Restricts to use magic module functions."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Checks that module hasn't magic module functions.

        All these functions are defined in ``MAGIC_MODULE_NAMES_BLACKLIST``
        """
        self._check_magic_module_functions(node)
        self.generic_visit(node)

    def _check_magic_module_functions(self, node: ast.FunctionDef) -> None:
        if self.options.i_control_code:
            if not isinstance(get_context(node), ast.Module):
                return

            if node.name in constants.MAGIC_MODULE_NAMES_BLACKLIST:
                self.add_violation(
                    BadMagicModuleFunctionViolation(node, text=node.name),
                )


@final
@alias('visit_any_assign', (
    'visit_Assign',
    'visit_AnnAssign',
))
class ModuleConstantsVisitor(BaseNodeVisitor):
    """Finds incorrect module constants."""

    _mutable_nodes: ClassVar[AnyNodes] = (
        ast.Dict,
        ast.List,
        ast.Set,
        ast.DictComp,
        ast.ListComp,
        ast.SetComp,
    )

    def visit_any_assign(self, node: AnyAssign) -> None:
        """Checks that module's cannot have incorrect constants."""
        self._check_mutable_constant(node)
        self.generic_visit(node)

    def _check_mutable_constant(self, node: AnyAssign) -> None:
        if not isinstance(get_context(node), ast.Module):
            return

        targets = cast(
            Iterable[ast.AST],
            [node.target] if isinstance(node, ast.AnnAssign) else node.targets,
        )

        for target in targets:
            if not isinstance(target, ast.Name) or not is_constant(target.id):
                continue

            if isinstance(node.value, self._mutable_nodes):
                self.add_violation(MutableModuleConstantViolation(target))
