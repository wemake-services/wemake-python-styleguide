import ast
import random
import copy

def main():
    file_to_read = 'test.py'
    with open(file_to_read, 'r') as f:
        program = ast.parse(f.read())

    collector = AllCollector()
    collector.visit(program)


class AllCollector(ast.NodeVisitor):

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self._check_BitOp(node)
        self.generic_visit(node)

    def _check_BitOp(self, node: ast.BinOp) -> None:
        if not isinstance(node.op, (ast.BitOr, ast.BitAnd)):
            return

        # print(node)

        print(node.left, node.right)
        print(self._check_sides(node.left) or self._check_sides(node.right))

    # checks either side of the Bitwise operation invalid usage
    def _check_sides(self, node) -> bool:
        invalid = False
        if not isinstance(node, (ast.Name, ast.Num)):
            invalid = True
        if isinstance(node, ast.NameConstant):
            invalid = True
        return invalid

    


if __name__ == '__main__':
    main()
