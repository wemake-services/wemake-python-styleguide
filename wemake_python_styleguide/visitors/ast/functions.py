import ast
from contextlib import suppress
from typing import ClassVar, Dict, FrozenSet, List, Mapping, Union

from typing_extensions import TypeAlias, final

from wemake_python_styleguide.compat.aliases import (
    ForNodes,
    FunctionNodes,
    TextNodes,
)
from wemake_python_styleguide.constants import (
    FUNCTIONS_BLACKLIST,
    LITERALS_BLACKLIST,
)
from wemake_python_styleguide.logic import nodes, source, walk
from wemake_python_styleguide.logic.arguments import function_args
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.logic.tree import (
    attributes,
    exceptions,
    functions,
    operators,
    stubs,
    variables,
)
from wemake_python_styleguide.types import (
    AnyFunctionDef,
    AnyFunctionDefAndLambda,
    AnyNodes,
)
from wemake_python_styleguide.violations import consistency, naming, oop
from wemake_python_styleguide.violations.best_practices import (
    BooleanPositionalArgumentViolation,
    ComplexDefaultValueViolation,
    FloatingNanViolation,
    GetterWithoutReturnViolation,
    PositionalOnlyArgumentsViolation,
    StopIterationInsideGeneratorViolation,
    WrongFunctionCallViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    ImplicitEnumerateViolation,
    ImplicitPrimitiveViolation,
    OpenWithoutContextManagerViolation,
    TypeCompareViolation,
    UselessLambdaViolation,
    WrongIsinstanceWithTupleViolation,
)
from wemake_python_styleguide.visitors import base, decorators

#: Things we treat as local variables.
_LocalVariable: TypeAlias = Union[ast.Name, ast.ExceptHandler]

#: Function definitions with name and arity:
_Defs: TypeAlias = Mapping[str, int]


@final
class WrongFunctionCallVisitor(base.BaseNodeVisitor):
    """
    Responsible for restricting some dangerous function calls.

    All these functions are defined in ``FUNCTIONS_BLACKLIST``.
    """

    _functions: ClassVar[_Defs] = {
        'getattr': 3,
        'setattr': 3,
    }

    _postfixes: ClassVar[_Defs] = {
        # dict methods:
        '.get': 2,
        '.pop': 2,
        '.setdefault': 2,

        # list methods:
        '.insert': 2,
    }

    def visit_Call(self, node: ast.Call) -> None:
        """Used to find ``FUNCTIONS_BLACKLIST`` calls."""
        self._check_wrong_function_called(node)
        self._check_boolean_arguments(node)
        self._check_isinstance_call(node)

        if functions.given_function_called(node, {'super'}):
            self._check_super_context(node)
            self._check_super_arguments(node)

        self.generic_visit(node)

    def _check_wrong_function_called(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(
            node, FUNCTIONS_BLACKLIST,
        )
        if function_name:
            self.add_violation(
                WrongFunctionCallViolation(node, text=function_name),
            )

    def _check_boolean_arguments(self, node: ast.Call) -> None:
        if len(node.args) == 1 and not node.keywords:
            return  # Calls with single boolean argument are allowed

        for arg in node.args:
            if not isinstance(arg, ast.NameConstant):
                continue

            is_ignored = self._is_call_ignored(node)

            # We do not check for `None` values here:
            if not is_ignored and arg.value in {True, False}:
                self.add_violation(
                    BooleanPositionalArgumentViolation(
                        arg, text=str(arg.value),
                    ),
                )

    def _check_isinstance_call(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, {'isinstance'})
        if not function_name or len(node.args) != 2:
            return

        if isinstance(node.args[1], ast.Tuple):
            if len(node.args[1].elts) == 1:
                self.add_violation(WrongIsinstanceWithTupleViolation(node))

    def _check_super_context(self, node: ast.Call) -> None:
        parent_context = nodes.get_context(node)
        parent_node = nodes.get_parent(node)

        attr = getattr(parent_node, 'attr', None)
        parent_name = getattr(parent_context, 'name', None)

        if attr and parent_name and attr != parent_name:
            self.add_violation(
                oop.WrongSuperCallAccessViolation(node),
            )

        if isinstance(parent_context, FunctionNodes):
            grand_context = nodes.get_context(parent_context)
            if isinstance(grand_context, ast.ClassDef):
                return

        self.add_violation(
            oop.WrongSuperCallViolation(node, text='not inside method'),
        )

    def _check_super_arguments(self, node: ast.Call) -> None:
        if node.args or node.keywords:
            self.add_violation(
                oop.WrongSuperCallViolation(node, text='remove arguments'),
            )

    def _is_call_ignored(self, node: ast.Call) -> bool:
        call = source.node_to_string(node.func)
        func_called = functions.given_function_called(
            node, self._functions.keys(),
        )

        return bool(
            func_called and len(node.args) == self._functions[func_called],
        ) or any(
            call.endswith(post)
            for post in self._postfixes
            if len(node.args) == self._postfixes[post]
        )


@final
class FloatingNanCallVisitor(base.BaseNodeVisitor):
    """Ensure that NaN explicitly acquired."""

    _nan_variants = frozenset(('nan', b'nan'))

    def visit_Call(self, node: ast.Call) -> None:
        """Used to find ``float("NaN")`` calls."""
        self._check_floating_nan(node)
        self.generic_visit(node)

    def _check_floating_nan(self, node: ast.Call) -> None:
        if len(node.args) != 1:
            return

        if not isinstance(node.args[0], (ast.Str, ast.Bytes)):
            return

        if not functions.given_function_called(node, 'float'):
            return

        if node.args[0].s.lower() in self._nan_variants:
            self.add_violation(FloatingNanViolation(node))


@final
class WrongFunctionCallContextVisitor(base.BaseNodeVisitor):
    """Ensure that we call several functions in the correct context."""

    def visit_Call(self, node: ast.Call) -> None:
        """Visits function calls to find wrong contexts."""
        self._check_open_call_context(node)
        self._check_type_compare(node)
        self._check_range_len(node)
        self.generic_visit(node)

    def _check_open_call_context(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, {'open'})
        if not function_name:
            return

        parent_node = nodes.get_parent(node)

        if isinstance(parent_node, ast.withitem):
            # We do not care about `with` or `async with` - both are fine.
            return

        if_exp_inside_with = (
            isinstance(parent_node, ast.IfExp) and
            isinstance(nodes.get_parent(parent_node), ast.withitem)
        )

        if if_exp_inside_with:
            return

        self.add_violation(OpenWithoutContextManagerViolation(node))

    def _check_type_compare(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(node, {'type'})
        if not function_name:
            return

        if isinstance(nodes.get_parent(node), ast.Compare):
            self.add_violation(TypeCompareViolation(node))

    def _check_range_len(self, node: ast.Call) -> None:
        if not isinstance(nodes.get_parent(node), ForNodes):
            return
        if not functions.given_function_called(node, {'range'}):
            return

        args_len = len(node.args)

        is_one_arg_range = (
            args_len == 1 and
            isinstance(node.args[0], ast.Call) and
            functions.given_function_called(node.args[0], {'len'})
        )
        is_two_args_range = (
            self._is_multiple_args_range_with_len(node) and
            args_len == 2
        )
        # for three args add violation
        # only if `step` arg do not equals 1 or -1
        step_arg = args_len == 3 and operators.unwrap_unary_node(node.args[2])
        is_three_args_range = (
            self._is_multiple_args_range_with_len(node) and
            args_len == 3 and
            isinstance(step_arg, ast.Num) and
            abs(step_arg.n) == 1
        )
        if any([is_one_arg_range, is_two_args_range, is_three_args_range]):
            self.add_violation(ImplicitEnumerateViolation(node))

    def _is_multiple_args_range_with_len(self, node: ast.Call) -> bool:
        return bool(
            len(node.args) in {2, 3} and
            isinstance(node.args[1], ast.Call) and
            functions.given_function_called(node.args[1], {'len'}),
        )


@final
@decorators.alias('visit_any_function', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class FunctionDefinitionVisitor(base.BaseNodeVisitor):
    """Responsible for checking function internals."""

    _descriptor_decorators: ClassVar[
        FrozenSet[str]
    ] = frozenset((
        'classmethod',
        'staticmethod',
        'property',
    ))

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Checks regular and ``async`` functions."""
        self._check_unused_variables(node)
        self._check_generator(node)
        self._check_descriptor_decorators(node)
        self.generic_visit(node)

    def _check_unused_variables(self, node: AnyFunctionDef) -> None:
        local_variables: Dict[str, List[_LocalVariable]] = {}

        for body_item in node.body:
            for sub_node in ast.walk(body_item):
                if isinstance(sub_node, (ast.Name, ast.ExceptHandler)):
                    var_name = variables.get_variable_name(sub_node)
                    self._maybe_update_variable(
                        sub_node, var_name, local_variables,
                    )

        self._ensure_used_variables(local_variables)

    def _check_generator(self, node: AnyFunctionDef) -> None:
        if not functions.is_generator(node):
            return

        for sub_node in walk.get_subnodes_by_type(node, ast.Raise):
            if exceptions.get_exception_name(sub_node) == 'StopIteration':
                self.add_violation(
                    StopIterationInsideGeneratorViolation(sub_node),
                )

    def _check_descriptor_decorators(self, node: AnyFunctionDef) -> None:
        if isinstance(nodes.get_parent(node), ast.ClassDef):
            return  # classes can contain descriptors

        descriptor_decorators = [
            decorator.id in self._descriptor_decorators
            for decorator in node.decorator_list
            if isinstance(decorator, ast.Name)
        ]

        if any(descriptor_decorators):
            self.add_violation(
                oop.WrongDescriptorDecoratorViolation(node),
            )

    def _maybe_update_variable(
        self,
        sub_node: _LocalVariable,
        var_name: str,
        local_variables: Dict[str, List[_LocalVariable]],
    ) -> None:
        defs = local_variables.get(var_name)
        if defs is not None:
            if not var_name or access.is_unused(var_name):
                # We check unused variable usage in a different place:
                # see `visitors/ast/naming.py`
                return
            defs.append(sub_node)
            return

        is_name_def = (
            isinstance(sub_node, ast.Name) and
            isinstance(sub_node.ctx, ast.Store)
        )

        if is_name_def or isinstance(sub_node, ast.ExceptHandler):
            local_variables[var_name] = []

    def _ensure_used_variables(
        self,
        local_variables: Mapping[str, List[_LocalVariable]],
    ) -> None:
        for varname, usages in local_variables.items():
            for node in usages:
                if access.is_protected(varname):
                    self.add_violation(
                        naming.UnusedVariableIsUsedViolation(
                            node, text=varname,
                        ),
                    )


@final
class UselessLambdaDefinitionVisitor(base.BaseNodeVisitor):
    """This visitor is used specifically for ``lambda`` functions."""

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """Checks if ``lambda`` functions are defined correctly."""
        self._check_useless_lambda(node)
        self._check_implicit_primitive(node)
        self.generic_visit(node)

    def _check_implicit_primitive(self, node: ast.Lambda) -> None:
        arguments = functions.get_all_arguments(node)
        if arguments:
            # We return from this check, since `lambda` has some arguments.
            return

        with suppress(ValueError):
            return_value = ast.literal_eval(node.body)
            if return_value is not None and not return_value:
                self.add_violation(ImplicitPrimitiveViolation(node))

    def _check_useless_lambda(self, node: ast.Lambda) -> None:
        if not isinstance(node.body, ast.Call):
            return
        if not isinstance(node.body.func, ast.Name):
            # We do not track method (attr) calls, since it might me complex.
            return

        if node.args.defaults or list(filter(None, node.args.kw_defaults)):
            # It means that `lambda` has defaults in args,
            # we cannot be sure that these defaults are the same
            # as in the call def, ignoring it.
            # `kw_defaults` can have [None, ...] items.
            return

        if not function_args.is_call_matched_by_arguments(node, node.body):
            return

        self.add_violation(UselessLambdaViolation(node))


@final
@decorators.alias('visit_any_function_and_lambda', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
    'visit_Lambda',
))
class FunctionSignatureVisitor(base.BaseNodeVisitor):
    """
    Checks function arguments and name when function is defined.

    Forbids to use ``/`` parameters in functions and lambdas.
    Forbids to use complex default arguments.
    Forbids to use getters with no output value.
    """

    _allowed_default_value_types: ClassVar[AnyNodes] = (
        *TextNodes,
        ast.Name,
        ast.Attribute,
        ast.NameConstant,
        ast.Tuple,
        ast.Num,
        ast.Ellipsis,
    )

    def visit_any_function_and_lambda(
        self,
        node: AnyFunctionDefAndLambda,
    ) -> None:
        """Checks function and lambda defs."""
        self._check_positional_arguments(node)
        self._check_complex_argument_defaults(node)
        if not isinstance(node, ast.Lambda):
            self._check_getter_without_return(node)
        self.generic_visit(node)

    def _check_getter_without_return(self, node: AnyFunctionDef) -> None:
        if not self._is_concrete_getter(node):
            return

        has_explicit_function_exit = False
        for function_exit_node in functions.get_function_exit_nodes(node):
            has_explicit_function_exit = True

            if function_exit_node.value is None:
                # Bare `yield` is allowed
                if isinstance(function_exit_node, ast.Yield):
                    continue
                self.add_violation(GetterWithoutReturnViolation(node))

        if not has_explicit_function_exit:
            self.add_violation(GetterWithoutReturnViolation(node))

    def _is_concrete_getter(self, node: AnyFunctionDef) -> bool:
        return (
            node.name.startswith('get_') and
            not stubs.is_stub(node)
        )

    def _check_positional_arguments(
        self,
        node: AnyFunctionDefAndLambda,
    ) -> None:
        if node.args.posonlyargs:
            self.add_violation(PositionalOnlyArgumentsViolation(node))

    def _check_complex_argument_defaults(
        self,
        node: AnyFunctionDefAndLambda,
    ) -> None:
        all_defaults = filter(None, (
            *node.args.defaults,
            *node.args.kw_defaults,
        ))

        for arg in all_defaults:
            real_arg = operators.unwrap_unary_node(arg)
            parts = attributes.parts(real_arg) if isinstance(
                real_arg, ast.Attribute,
            ) else [real_arg]

            has_incorrect_part = any(
                not isinstance(part, self._allowed_default_value_types)
                for part in parts
            )

            if has_incorrect_part:
                self.add_violation(ComplexDefaultValueViolation(arg))


@final
class UnnecessaryLiteralsVisitor(base.BaseNodeVisitor):
    """
    Responsible for restricting some literals.

    All these literals are defined in ``LITERALS_BLACKLIST``.
    """

    def visit_Call(self, node: ast.Call) -> None:
        """Used to find ``LITERALS_BLACKLIST`` without args calls."""
        self._check_unnecessary_literals(node)
        self.generic_visit(node)

    def _check_unnecessary_literals(self, node: ast.Call) -> None:
        function_name = functions.given_function_called(
            node, LITERALS_BLACKLIST,
        )
        if function_name and not node.args:
            self.add_violation(consistency.UnnecessaryLiteralsViolation(node))
