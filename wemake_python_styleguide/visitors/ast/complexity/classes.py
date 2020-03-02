import ast
from collections import defaultdict
from typing import DefaultDict

from typing_extensions import final

from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.complexity import (
    TooManyBaseClassesViolation,
    TooManyMethodsViolation,
    TooManyPublicAttributesViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
class ClassComplexityVisitor(BaseNodeVisitor):
    """Checks class complexity."""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Checking class definitions.

        We don't check ``NamedExpr`` here, because it is a syntax error
        to assign values to attributes.

        .. code:: python

            class T:
                def t(self):
                    if self.a := True:
                        print(self.a)

            File "<stdin>", line 3
            SyntaxError: cannot use named assignment with attribute

        Raises:
            TooManyBaseClassesViolation
            TooManyPublicAttributesViolation

        """
        self._check_base_classes(node)
        self._check_public_attributes(node)
        self.generic_visit(node)

    def _check_base_classes(self, node: ast.ClassDef) -> None:
        if len(node.bases) > self.options.max_base_classes:
            self.add_violation(
                TooManyBaseClassesViolation(
                    node,
                    text=str(len(node.bases)),
                    baseline=self.options.max_base_classes,
                ),
            )

    def _check_public_attributes(self, node: ast.ClassDef) -> None:
        attributes = filter(
            self._is_public_instance_attr_def,
            walk.get_subnodes_by_type(node, ast.Attribute),
        )
        attrs_count = len({attr.attr for attr in attributes})
        if attrs_count > self.options.max_attributes:
            self.add_violation(
                TooManyPublicAttributesViolation(
                    node,
                    text=str(attrs_count),
                    baseline=self.options.max_attributes,
                ),
            )

    def _is_public_instance_attr_def(self, node: ast.Attribute) -> bool:
        return (
            isinstance(node.ctx, ast.Store) and
            access.is_public(node.attr) and
            isinstance(node.value, ast.Name) and
            node.value.id == 'self'
        )


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class MethodMembersVisitor(BaseNodeVisitor):
    """Counts methods in a single class."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates a counter for tracked methods in different classes."""
        super().__init__(*args, **kwargs)
        self._methods: DefaultDict[ast.ClassDef, int] = defaultdict(int)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """
        Counts the number of methods in a single class.

        Raises:
            TooManyMethodsViolation

        """
        self._check_method(node)
        self.generic_visit(node)

    def _check_method(self, node: AnyFunctionDef) -> None:
        parent = get_parent(node)
        if isinstance(parent, ast.ClassDef):
            self._methods[parent] += 1

    def _post_visit(self) -> None:
        for node, count in self._methods.items():
            if count > self.options.max_methods:
                self.add_violation(
                    TooManyMethodsViolation(
                        node,
                        text=str(count),
                        baseline=self.options.max_methods,
                    ),
                )
