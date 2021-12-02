import ast
from typing import ClassVar, FrozenSet

from typing_extensions import final

from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.violations.best_practices import (
    ProtectedAttributeViolation,
)
from wemake_python_styleguide.violations.oop import (
    DirectMagicAttributeAccessViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class WrongAttributeVisitor(BaseNodeVisitor):
    """Ensures that attributes are used correctly."""

    _allowed_to_use_protected: ClassVar[FrozenSet[str]] = frozenset((
        'self',
        'cls',
        'mcs',
    ))

    _disallowed_magic_attributes: ClassVar[FrozenSet[str]] = frozenset((
        # docs.python.org/3/reference/datamodel.html#special-method-names
        '__new__',
        '__init__',
        '__del__',
        '__repr__',
        '__str__',
        '__unicode__',
        '__bytes__',
        '__format__',
        '__cmp__',
        '__lt__',
        '__le__',
        '__eq__',
        '__ne__',
        '__gt__',
        '__ge__',
        '__hash__',
        '__bool__',
        '__nonzero__',
        '__getattr__',
        '__getattribute__',
        '__setattr__',
        '__delattr__',
        '__dir__',
        '__sizeof__',
        '__get__',
        '__set__',
        '__delete__',
        '__init_subclass__',
        '__set_name__',
        '__instancecheck__',
        '__subclasscheck__',
        '__class_getitem__',
        '__call__',
        '__len__',
        '__length_hint__',
        '__getitem__',
        '__setitem__',
        '__missing__',
        '__iter__',
        '__next__',
        '__reversed__',
        '__contains__',
        '__add__',
        '__sub__',
        '__mul__',
        '__matmul__',
        '__truediv__',
        '__floordiv__',
        '__mod__',
        '__divmod__',
        '__pow__',
        '__lshift__',
        '__rshift__',
        '__and__',
        '__xor__',
        '__or__',
        '__radd__',
        '__rsub__',
        '__rmul__',
        '__rmatmul__',
        '__rtruediv__',
        '__rfloordiv__',
        '__rmod__',
        '__rdivmod__',
        '__rpow__',
        '__rlshift__',
        '__rrshift__',
        '__rand__',
        '__rxor__',
        '__ror__',
        '__iadd__',
        '__isub__',
        '__imul__',
        '__imatmul__',
        '__itruediv__',
        '__ifloordiv__',
        '__imod__',
        '__ipow__',
        '__ilshift__',
        '__irshift__',
        '__iand__',
        '__ixor__',
        '__ior__',
        '__neg__',
        '__pos__',
        '__abs__',
        '__invert__',
        '__complex__',
        '__int__',
        '__long__',
        '__float__',
        '__hex__',
        '__oct__',
        '__index__',
        '__round__',
        '__trunc__',
        '__coerce__',
        '__floor__',
        '__ceil__',
        '__enter__',
        '__exit__',
        '__await__',
        '__aiter__',
        '__anext__',
        '__aenter__',
        '__aexit__',

        # pickling
        '__getnewargs_ex__',
        '__getnewargs__',
        '__getstate__',
        '__setstate__',
        '__reduce__',
        '__reduce_ex__',
        '__getinitargs__',

        # copy
        '__copy__',
        '__deepcopy__',

        # dataclasses
        '__post_init__',

        # inspect
        '__signature__',

        # os.path
        '__fspath__',
    ))

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Checks the `Attribute` node."""
        self._check_protected_attribute(node)
        self._check_magic_attribute(node)
        self.generic_visit(node)

    def _is_super_called(self, node: ast.Call) -> bool:
        return isinstance(node.func, ast.Name) and node.func.id == 'super'

    def _ensure_attribute_type(self, node: ast.Attribute, exception) -> None:
        if isinstance(node.value, ast.Name):
            if node.value.id in self._allowed_to_use_protected:
                return

        if isinstance(node.value, ast.Call):
            if self._is_super_called(node.value):
                return

        self.add_violation(exception(node, text=node.attr))

    def _check_protected_attribute(self, node: ast.Attribute) -> None:
        if access.is_protected(node.attr):
            self._ensure_attribute_type(node, ProtectedAttributeViolation)

    def _check_magic_attribute(self, node: ast.Attribute) -> None:
        if access.is_magic(node.attr):
            if node.attr in self._disallowed_magic_attributes:
                self._ensure_attribute_type(
                    node, DirectMagicAttributeAccessViolation,
                )
