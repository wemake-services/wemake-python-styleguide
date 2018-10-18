ast_nodes = [
    target
    for assignment in top_level_assigns
    for target in assignment.targets
    for _ in range(10)
    if isinstance(target, ast.Name) and is_upper_case_name(target.id)
]
