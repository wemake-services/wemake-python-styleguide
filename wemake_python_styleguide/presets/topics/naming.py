from typing_extensions import Final

from wemake_python_styleguide.visitors.ast.naming import validation, variables

#: Used to store all naming related visitors to be later passed to checker:
PRESET: Final = (
    validation.WrongNameVisitor,

    variables.WrongModuleMetadataVisitor,
    variables.WrongVariableAssignmentVisitor,
    variables.UnusedVariableUsageVisitor,
    variables.UnusedVariableDefinitionVisitor,
)
