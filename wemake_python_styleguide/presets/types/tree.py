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
    subscripts,
)

#: Used to store all general visitors to be later passed to checker:
PRESET: Final = (
    # General:
    statements.StatementsWithBodiesVisitor,
    statements.WrongParametersIndentationVisitor,
    statements.PointlessStarredVisitor,
    statements.WrongNamedKeywordVisitor,
    statements.AssignmentPatternsVisitor,
    statements.WrongMethodArgumentsVisitor,

    keywords.WrongRaiseVisitor,
    keywords.WrongKeywordVisitor,
    keywords.WrongContextManagerVisitor,
    keywords.ConsistentReturningVisitor,
    keywords.ConsistentReturningVariableVisitor,
    keywords.ConstantKeywordVisitor,
    keywords.GeneratorKeywordsVisitor,

    loops.WrongComprehensionVisitor,
    loops.WrongLoopVisitor,
    loops.WrongLoopDefinitionVisitor,
    loops.SyncForLoopVisitor,

    attributes.WrongAttributeVisitor,
    annotations.WrongAnnotationVisitor,

    functions.WrongFunctionCallVisitor,
    functions.FunctionDefinitionVisitor,
    functions.UselessLambdaDefinitionVisitor,
    functions.WrongFunctionCallContextVisitior,
    functions.UnnecessaryLiteralsVisitor,

    exceptions.WrongTryExceptVisitor,
    exceptions.NestedTryBlocksVisitor,
    exceptions.WrongExceptHandlerVisitor,

    imports.WrongImportVisitor,

    naming.WrongNameVisitor,
    naming.WrongModuleMetadataVisitor,
    naming.WrongVariableAssignmentVisitor,
    naming.WrongVariableUsageVisitor,

    builtins.WrongNumberVisitor,
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
    compares.InCompareSanityVisitor,

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

    subscripts.SubscriptVisitor,
    subscripts.ImplicitDictGetVisitor,
    subscripts.CorrectKeyVisitor,

    # Complexity:
    *complexity.PRESET,
)
