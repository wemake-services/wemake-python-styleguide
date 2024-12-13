# Copied from `pep8-naming`
# https://github.com/PyCQA/pep8-naming

# Original license

# Copyright © 2013 Florent Xicluna <florent.xicluna@gmail.com>
# Licensed under the terms of the Expat License

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ast
from typing import final


# @final
# class NamingChecker:
#     """Checker of PEP-8 Naming Conventions."""

#     def __init__(self, tree: ast.AST, filename: str) -> None:
#         self.tree = tree

#     @classmethod
#     def parse_options(cls, options):
#         cls.ignore_names = frozenset(options.ignore_names)
#         cls.decorator_to_type = _build_decorator_to_type(
#             options.classmethod_decorators,
#             options.staticmethod_decorators)

#         # Build a list of node visitors based the error codes that have been
#         # selected in the style guide. Only the checks that have been selected
#         # will be evaluated as a performance optimization.
#         engine = style_guide.DecisionEngine(options)
#         cls.visitors = frozenset(
#             visitor for visitor in BaseASTCheck.all for code in visitor.codes
#             if engine.decision_for(code) is style_guide.Decision.Selected
#         )

#     def run(self):
#         return self.visit_tree(self.tree, deque()) if self.tree else ()

#     def visit_tree(self, node, parents: deque):
#         yield from self.visit_node(node, parents)
#         parents.append(node)
#         for child in iter_child_nodes(node):
#             yield from self.visit_tree(child, parents)
#         parents.pop()

#     def visit_node(self, node, parents: Iterable):
#         if isinstance(node, ast.ClassDef):
#             self.tag_class_functions(node)
#         elif isinstance(node, FUNC_NODES):
#             self.find_global_defs(node)

#         method = 'visit_' + node.__class__.__name__.lower()
#         ignore_names = self.ignore_names
#         for visitor in self.visitors:
#             visitor_method = getattr(visitor, method, None)
#             if visitor_method is None:
#                 continue
#             yield from visitor_method(node, parents, ignore_names)

#     def tag_class_functions(self, cls_node):
#         """Tag functions if they are methods, classmethods, staticmethods"""
#         # tries to find all 'old style decorators' like
#         # m = staticmethod(m)
#         late_decoration = {}
#         for node in iter_child_nodes(cls_node):
#             if not (isinstance(node, ast.Assign) and
#                     isinstance(node.value, ast.Call) and
#                     isinstance(node.value.func, ast.Name)):
#                 continue
#             func_name = node.value.func.id
#             if func_name not in self.decorator_to_type:
#                 continue
#             meth = (len(node.value.args) == 1 and node.value.args[0])
#             if isinstance(meth, ast.Name):
#                 late_decoration[meth.id] = self.decorator_to_type[func_name]

#         # If this class inherits from a known metaclass base class, it is
#         # itself a metaclass, and we'll consider all of its methods to be
#         # classmethods.
#         bases = chain(
#             (b.id for b in cls_node.bases if isinstance(b, ast.Name)),
#             (b.attr for b in cls_node.bases if isinstance(b, ast.Attribute)),
#         )
#         ismetaclass = any(name for name in bases if name in METACLASS_BASES)

#         self.set_function_nodes_types(
#             iter_child_nodes(cls_node), ismetaclass, late_decoration)

#     def set_function_nodes_types(self, nodes, ismetaclass, late_decoration):
#         # iterate over all functions and tag them
#         for node in nodes:
#             if type(node) in METHOD_CONTAINER_NODES:
#                 self.set_function_nodes_types(
#                     iter_child_nodes(node), ismetaclass, late_decoration)
#             if not isinstance(node, FUNC_NODES):
#                 continue
#             node.function_type = _FunctionType.METHOD
#             if node.name in CLASS_METHODS or ismetaclass:
#                 node.function_type = _FunctionType.CLASSMETHOD
#             if node.name in late_decoration:
#                 node.function_type = late_decoration[node.name]
#             elif node.decorator_list:
#                 for d in node.decorator_list:
#                     name = self.find_decorator_name(d)
#                     if name in self.decorator_to_type:
#                         node.function_type = self.decorator_to_type[name]
#                         break

#     @classmethod
#     def find_decorator_name(cls, d):
#         if isinstance(d, ast.Name):
#             return d.id
#         elif isinstance(d, ast.Attribute):
#             return d.attr
#         elif isinstance(d, ast.Call):
#             return cls.find_decorator_name(d.func)

#     @staticmethod
#     def find_global_defs(func_def_node):
#         global_names = set()
#         nodes_to_check = deque(iter_child_nodes(func_def_node))
#         while nodes_to_check:
#             node = nodes_to_check.pop()
#             if isinstance(node, ast.Global):
#                 global_names.update(node.names)

#             if not isinstance(node, (ast.ClassDef,) + FUNC_NODES):
#                 nodes_to_check.extend(iter_child_nodes(node))
#         func_def_node.global_names = global_names
