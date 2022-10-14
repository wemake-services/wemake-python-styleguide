from typing_extensions import Final

from wemake_python_styleguide.presets.topics import complexity, naming
from wemake_python_styleguide.visitors.ast import (  # noqa: WPS235
    annotations,
    attributes,
    blocks,
    builtins,
    classes,
    compares,
    conditions,
    decorators,
    exceptions,
    function_empty_lines,
    functions,
    imports,
    iterables,
    keywords,
    loops,
    modules,
    operators,
    redundancy,
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
    functions.WrongFunctionCallContextVisitor,
    functions.UnnecessaryLiteralsVisitor,
    functions.FunctionSignatureVisitor,
    functions.FloatingNanCallVisitor,

    exceptions.WrongTryExceptVisitor,
    exceptions.NestedTryBlocksVisitor,
    exceptions.WrongExceptHandlerVisitor,

    imports.WrongImportVisitor,

    builtins.WrongNumberVisitor,
    builtins.WrongStringVisitor,
    builtins.WrongFormatStringVisitor,
    builtins.WrongAssignmentVisitor,
    builtins.WrongCollectionVisitor,

    operators.UselessOperatorsVisitor,
    operators.WrongMathOperatorVisitor,
    operators.WalrusVisitor,
    operators.BitwiseOpVisitor,

    compares.WrongConditionalVisitor,
    compares.CompareSanityVisitor,
    compares.WrongComparisonOrderVisitor,
    compares.UnaryCompareVisitor,
    compares.WrongConstantCompareVisitor,
    compares.InCompareSanityVisitor,
    compares.WrongFloatComplexCompareVisitor,

    conditions.IfStatementVisitor,
    conditions.BooleanConditionVisitor,
    conditions.ImplicitBoolPatternsVisitor,
    conditions.UselessElseVisitor,
    conditions.ChainedIsVisitor,

    iterables.IterableUnpackingVisitor,

    classes.WrongClassDefVisitor,
    classes.WrongClassBodyVisitor,
    classes.WrongMethodVisitor,
    classes.WrongSlotsVisitor,
    classes.ClassAttributeVisitor,
    classes.ClassMethodOrderVisitor,
    classes.BuggySuperCallVisitor,

    blocks.BlockVariableVisitor,
    blocks.AfterBlockVariablesVisitor,

    subscripts.SubscriptVisitor,
    subscripts.ImplicitDictGetVisitor,
    subscripts.CorrectKeyVisitor,

    decorators.WrongDecoratorVisitor,

    redundancy.RedundantEnumerateVisitor,

    function_empty_lines.WrongEmptyLinesCountVisitor,

    # Modules:
    modules.EmptyModuleContentsVisitor,
    modules.MagicModuleFunctionsVisitor,
    modules.ModuleConstantsVisitor,

    # Topics:
    *complexity.PRESET,
    *naming.PRESET,
)
