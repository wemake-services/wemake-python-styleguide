# -*- coding: utf-8 -*-

from typing_extensions import Final

from wemake_python_styleguide.presets.topics import complexity
from wemake_python_styleguide.visitors.ast import (
    annotations,
    attributes,
    blocks,
    builtins,
    classes,
    compares,
    conditions,
    exceptions,
    functions,
    imports,
    keywords,
    loops,
    modules,
    naming,
    operators,
    statements,
)

#: Used to store all general visitors to be later passed to checker:
PRESET: Final = (
    # General:
    statements.StatementsWithBodiesVisitor,
    statements.WrongParametersIndentationVisitor,
    statements.PointlessStarredVisitor,

    keywords.WrongRaiseVisitor,
    keywords.WrongKeywordVisitor,
    keywords.WrongContextManagerVisitor,
    keywords.ConsistentReturningVisitor,
    keywords.ConsistentReturningVariableVisitor,
    keywords.ConstantKeywordVisitor,

    loops.WrongComprehensionVisitor,
    loops.WrongLoopVisitor,
    loops.WrongLoopDefinitionVisitor,

    attributes.WrongAttributeVisitor,
    annotations.WrongAnnotationVisitor,

    functions.WrongFunctionCallVisitor,
    functions.FunctionDefinitionVisitor,
    functions.UselessLambdaDefinitionVisitor,
    functions.WrongFunctionCallContextVisitior,

    exceptions.WrongTryExceptVisitor,
    exceptions.NestedTryBlocksVisitor,

    imports.WrongImportVisitor,

    naming.WrongNameVisitor,
    naming.WrongModuleMetadataVisitor,
    naming.WrongVariableAssignmentVisitor,
    naming.WrongVariableUsageVisitor,

    builtins.MagicNumberVisitor,
    builtins.WrongStringVisitor,
    builtins.WrongAssignmentVisitor,
    builtins.WrongCollectionVisitor,

    operators.UselessOperatorsVisitor,
    operators.WrongMathOperatorVisitor,

    compares.WrongConditionalVisitor,
    compares.CompareSanityVisitor,
    compares.WrongComparisionOrderVisitor,
    compares.UnaryCompareVisitor,
    compares.WrongConstantCompareVisitor,

    conditions.IfStatementVisitor,
    conditions.BooleanConditionVisitor,
    conditions.ImplicitBoolPatternsVisitor,

    # Classes:
    classes.WrongClassVisitor,
    classes.WrongMethodVisitor,
    classes.WrongSlotsVisitor,
    classes.ClassAttributeVisitor,
    classes.ClassMethodOrderVisitor,

    # Modules:
    modules.EmptyModuleContentsVisitor,
    modules.MagicModuleFunctionsVisitor,
    modules.ModuleConstantsVisitor,

    # Blocks:
    blocks.BlockVariableVisitor,
    blocks.AfterBlockVariablesVisitor,

    # Complexity:
    *complexity.PRESET,
)
