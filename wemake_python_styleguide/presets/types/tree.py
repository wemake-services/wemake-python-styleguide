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
    statements,
)

#: Used to store all general visitors to be later passed to checker:
PRESET: Final = (
    # General:
    statements.StatementsWithBodiesVisitor,
    statements.WrongParametersIndentationVisitor,

    keywords.WrongRaiseVisitor,
    keywords.WrongKeywordVisitor,
    keywords.WrongContextManagerVisitor,
    keywords.ConsistentReturningVisitor,
    keywords.ConsistentReturningVariableVisitor,

    loops.WrongComprehensionVisitor,
    loops.WrongLoopVisitor,
    loops.WrongLoopDefinitionVisitor,

    attributes.WrongAttributeVisitor,
    annotations.WrongAnnotationVisitor,

    functions.WrongFunctionCallVisitor,
    functions.FunctionDefinitionVisitor,
    functions.UselessLambdaDefinitionVisitor,

    exceptions.WrongTryExceptVisitor,
    exceptions.NestedTryBlocksVisitor,

    imports.WrongImportVisitor,

    naming.WrongNameVisitor,
    naming.WrongModuleMetadataVisitor,
    naming.WrongVariableAssignmentVisitor,

    builtins.MagicNumberVisitor,
    builtins.UselessOperatorsVisitor,
    builtins.WrongStringVisitor,
    builtins.WrongAssignmentVisitor,
    builtins.WrongCollectionVisitor,

    compares.WrongConditionalVisitor,
    compares.CompareSanityVisitor,
    compares.WrongComparisionOrderVisitor,
    compares.UnaryCompareVisitor,

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
