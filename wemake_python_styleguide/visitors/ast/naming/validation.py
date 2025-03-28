import ast
from collections.abc import Callable, Iterable
from typing import ClassVar, TypeAlias, final

import attr

from wemake_python_styleguide.compat.functions import (
    get_assign_targets,
    get_type_param_names,
)
from wemake_python_styleguide.compat.nodes import TypeAlias as TypeAliasNode
from wemake_python_styleguide.compat.types import NamedMatch, NodeWithTypeParams
from wemake_python_styleguide.constants import (
    SPECIAL_ARGUMENT_NAMES_WHITELIST,
    UNREADABLE_CHARACTER_COMBINATIONS,
)
from wemake_python_styleguide.logic.naming import (
    access,
    alphabet,
    blacklists,
    builtins,
    enums,
    logical,
    name_nodes,
)
from wemake_python_styleguide.logic.tree import (
    attributes,
    classes,
    functions,
)
from wemake_python_styleguide.options.validation import ValidatedOptions
from wemake_python_styleguide.types import (
    AnyAssign,
    AnyFunctionDefAndLambda,
    AnyImport,
    AnyVariableDef,
)
from wemake_python_styleguide.violations import base, naming
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

_ErrorCallback: TypeAlias = Callable[[base.BaseViolation], None]

_PredicateApplicableCallback: TypeAlias = Callable[[ast.AST], bool]
_PredicateLogicalCallback: TypeAlias = Callable[[str], bool]


@final
@attr.dataclass(slots=True, frozen=True)
class _NamingPredicate:
    """Structure we use to apply different naming rules to variable names."""

    is_correct: _PredicateLogicalCallback
    violation: type[base.BaseViolation]

    _is_applicable: _PredicateApplicableCallback | None = None

    def is_applicable(self, node: ast.AST) -> bool:
        """Usability function over real applicable predicate."""
        return self._is_applicable is None or self._is_applicable(node)


class _SimpleNameValidator:
    """Utility class to separate logic from the naming visitor."""

    _naming_predicates: ClassVar[Iterable[_NamingPredicate]] = (
        _NamingPredicate(
            access.is_private,
            naming.PrivateNameViolation,
        ),
        _NamingPredicate(
            lambda name: access.is_unused(name) and len(name) > 1,
            naming.WrongUnusedVariableNameViolation,
        ),
    )

    def __init__(
        self,
        error_callback: _ErrorCallback,
        options: ValidatedOptions,
    ) -> None:
        """Creates new instance of a name validator."""
        self._error_callback = error_callback
        self._options = options
        self._variable_names_blacklist = (
            blacklists.variable_names_blacklist_from(options)
        )

    def check_name(
        self,
        node: ast.AST,
        name: str,
        *,
        is_first_argument: bool = False,
    ) -> None:
        for predicate in self._naming_predicates:
            if predicate.is_applicable(node) and predicate.is_correct(name):
                self._error_callback(predicate.violation(node, text=name))

        self._ensure_reserved_name(
            node,
            name,
            is_first_argument=is_first_argument,
        )

    def _ensure_reserved_name(
        self,
        node: ast.AST,
        name: str,
        *,
        is_first_argument: bool,
    ) -> None:
        if is_first_argument:
            return

        if name not in SPECIAL_ARGUMENT_NAMES_WHITELIST:
            return

        self._error_callback(
            naming.ReservedArgumentNameViolation(node, text=name),
        )


class _RegularNameValidator(_SimpleNameValidator):
    _naming_predicates: ClassVar[Iterable[_NamingPredicate]] = (
        *_SimpleNameValidator._naming_predicates,  # noqa: SLF001
        _NamingPredicate(
            builtins.is_wrong_alias,
            naming.TrailingUnderscoreViolation,
        ),
        _NamingPredicate(
            alphabet.does_contain_underscored_number,
            naming.UnderscoredNumberNameViolation,
        ),
        _NamingPredicate(
            alphabet.does_contain_consecutive_underscores,
            naming.ConsecutiveUnderscoresInNameViolation,
        ),
    )

    def check_name(
        self,
        node: ast.AST,
        name: str,
        *,
        is_first_argument: bool = False,
    ) -> None:
        super().check_name(node, name, is_first_argument=is_first_argument)

        self._ensure_length(node, name)
        self._ensure_correct_name(node, name)
        self._ensure_readable_name(node, name)

    def _ensure_length(self, node: ast.AST, name: str) -> None:
        if (
            logical.is_too_short_name(
                name,
                min_length=self._options.min_name_length,
            )
            and name not in self._options.allowed_domain_names
        ):
            self._error_callback(
                naming.TooShortNameViolation(
                    node,
                    text=name,
                    baseline=self._options.min_name_length,
                ),
            )

        if logical.is_too_long_name(
            name,
            max_length=self._options.max_name_length,
        ):
            self._error_callback(
                naming.TooLongNameViolation(
                    node,
                    text=name,
                    baseline=self._options.max_name_length,
                ),
            )

    def _ensure_correct_name(self, node: ast.AST, name: str) -> None:
        if logical.is_wrong_name(name, self._variable_names_blacklist):
            self._error_callback(
                naming.WrongVariableNameViolation(node, text=name),
            )

    def _ensure_readable_name(self, node: ast.AST, name: str) -> None:
        unreadable_sequence = alphabet.get_unreadable_characters(
            name,
            UNREADABLE_CHARACTER_COMBINATIONS,
        )
        if unreadable_sequence:
            self._error_callback(
                naming.UnreadableNameViolation(node, text=unreadable_sequence),
            )


@final
class _FunctionNameValidator(_RegularNameValidator):
    def check_function_signature(self, node: AnyFunctionDefAndLambda) -> None:
        for arg in functions.get_all_arguments(node):
            is_first_argument = functions.is_first_argument(
                node,
                arg.arg,
            ) and not isinstance(node, ast.Lambda)
            self.check_name(
                arg,
                arg.arg,
                is_first_argument=is_first_argument,
            )


@final
class _TypeParamNameValidator(_RegularNameValidator):
    def check_type_params(  # pragma: >=3.12 cover
        self,
        node: NodeWithTypeParams,
    ) -> None:
        for type_param_node, type_param_name in get_type_param_names(node):
            self.check_name(type_param_node, type_param_name)


@final
class _ClassBasedNameValidator(_RegularNameValidator):
    def check_attribute_names(self, node: ast.ClassDef) -> None:
        class_attributes, _ = classes.get_attributes(
            node,
            include_annotated=True,
        )
        is_enum_like = enums.has_enum_like_base(node)

        for assign in class_attributes:
            for target in get_assign_targets(assign):
                for attr_name in name_nodes.get_variables_from_node(target):
                    self._ensure_case(
                        assign,
                        attr_name,
                        is_enum_like=is_enum_like,
                    )

    def _ensure_case(
        self,
        node: AnyAssign,
        name: str,
        *,
        is_enum_like: bool,
    ) -> None:
        if not is_enum_like and logical.is_upper_case_name(name):
            self._error_callback(
                naming.UpperCaseAttributeViolation(node, text=name),
            )


@final
@alias(
    'visit_any_import',
    (
        'visit_ImportFrom',
        'visit_Import',
    ),
)
@alias(
    'visit_variable',
    (
        'visit_Name',
        'visit_Attribute',
        'visit_ExceptHandler',
    ),
)
@alias(
    'visit_any_function',
    (
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
        'visit_Lambda',
    ),
)
@alias(
    'visit_named_match',
    (
        'visit_MatchStar',
        'visit_MatchAs',
    ),
)
class WrongNameVisitor(BaseNodeVisitor):
    """Performs checks based on variable names."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes new naming validator for this visitor."""
        super().__init__(*args, **kwargs)
        self._simple_validator = _SimpleNameValidator(
            self.add_violation,
            self.options,
        )
        self._regular_validator = _RegularNameValidator(
            self.add_violation,
            self.options,
        )
        self._function_validator = _FunctionNameValidator(
            self.add_violation,
            self.options,
        )
        self._class_based_validator = _ClassBasedNameValidator(
            self.add_violation,
            self.options,
        )
        self._type_params_validator = _TypeParamNameValidator(
            self.add_violation,
            self.options,
        )

    def visit_any_import(self, node: AnyImport) -> None:
        """Used to check wrong import alias names."""
        for alias_node in node.names:
            if alias_node.asname:
                self._regular_validator.check_name(node, alias_node.asname)
        self.generic_visit(node)

    def visit_variable(self, node: AnyVariableDef) -> None:
        """Used to check wrong names of assigned."""
        validator = (
            self._simple_validator
            if attributes.is_foreign_attribute(
                node,
            )
            else self._regular_validator
        )

        variable_name = name_nodes.get_assigned_name(node)
        if variable_name is not None:
            validator.check_name(node, variable_name)
        self.generic_visit(node)

    def visit_any_function(self, node: AnyFunctionDefAndLambda) -> None:
        """Used to find wrong function and method parameters."""
        if not isinstance(node, ast.Lambda):
            self._function_validator.check_name(node, node.name)
            self._type_params_validator.check_type_params(node)
        self._function_validator.check_function_signature(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Used to find upper attribute declarations."""
        self._class_based_validator.check_name(node, node.name)
        self._class_based_validator.check_attribute_names(node)
        self._type_params_validator.check_type_params(node)
        self.generic_visit(node)

    def visit_named_match(self, node: NamedMatch) -> None:
        """
        Check pattern matching.

        In a form of
        - `case ... as NAME`
        - `case [*NAME]`
        - `case {**NAME}`

        """
        if node.name:
            self._regular_validator.check_name(node, node.name)
        self.generic_visit(node)

    def visit_TypeAlias(
        self,
        node: TypeAliasNode,
    ) -> None:  # pragma: >=3.12 cover
        """Visit PEP695 type aliases."""
        self._type_params_validator.check_type_params(node)
        self.generic_visit(node)
