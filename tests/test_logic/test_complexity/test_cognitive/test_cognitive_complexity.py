# -*- coding: utf-8 -*-

"""
Test to ensure that we count cognitive complexity correctly.

Adapted from https://github.com/Melevir/cognitive_complexity
"""

import pytest

complexity1_1 = """
def f(a, b):
    if a:  # +1
        return 1
"""

complexity1_2 = """
def f(a):
    return a * f(a - 1)  # +1 for recursion
"""

complexity2_1 = """
def f(a, b):
    if a and b and True:  # +2
        return 1
"""

complexity2_2 = """
def f(a, b):
    if (a):  # +1
        return 1
    if b:  # +1
        return 2
"""

complexity3_1 = """
def f(a, b):
    if a and b or True:  # +3
        return 1
"""

complexity3_2 = """
def f(a, b):
    if (  # +1
        a and b and  # +1
        (c or d)  # +1
    ):
        return 1
"""

complexity3_3 = """
def f(a, b):
    if a:  # +1
        for i in range(b):  # +2
            return 1
"""

complexity4_1 = """
def f(a, b):
    try:
        for foo in bar:  # +1
            return a
    except Exception:  # +1
        if a < 0:  # +2
            return a
"""

complexity4_2 = """
def f(a):
    def foo(a):
        if a:  # +2
            return 1
    bar = lambda a: lambda b: b or 2  # +2
    return bar(foo(a))(a)
"""

complexity4_3 = """
def f(a):
    if a % 2:  # +1
        return 'c' if a else 'd'  # +2
    return 'a' if a else 'b'  # +1
"""

complexity6_1 = """
def f(a, b):
    if a:  # +1
        for i in range(b):  # +2
            if b:  # +3
                return 1
"""

complexity9_1 = """
def f(a):
    for a in range(10):  # +1
        if a % 2:  # +2
            continue  # +2
        if a == 8:  # +2
            break  # +2
"""

complexity10_1 = """
def process_raw_constant(constant, min_word_length):
    processed_words = []
    raw_camelcase_words = []
    for raw_word in re.findall(r'[a-z]+', constant):  # +1
        word = raw_word.strip()
        if (  # +2
            len(word) >= min_word_length  # +4
            and not (word.startswith('-') or word.endswith('-'))
        ):
            if is_camel_case_word(word):  # +3
                raw_camelcase_words.append(word)
            else:
                processed_words.append(word.lower())
    return processed_words, raw_camelcase_words
"""

complexity14_1 = """
def enhance(tree):
    for statement in ast.walk(tree):  # +1
        if not isinstance(statement, ast.If):  # +2
            continue  # +2

        for child in ast.iter_child_nodes(statement): # +2
            if isinstance(child, ast.If):  # +3
                if child in statement.orelse:  # +4
                    setattr(statement, 'wps_if_chained', True)
                    setattr(child, 'wps_if_chain', statement)
    return tree
"""


@pytest.mark.parametrize(('code', 'complexity'), [
    (complexity1_1, 1),
    (complexity1_2, 1),

    (complexity2_1, 2),
    (complexity2_2, 2),

    (complexity3_1, 3),
    (complexity3_2, 3),
    (complexity3_3, 3),

    (complexity4_1, 4),
    (complexity4_2, 4),
    (complexity4_3, 4),

    (complexity6_1, 6),
    (complexity9_1, 9),
    (complexity10_1, 10),
    (complexity14_1, 14),
])
def test_cognitive_complexity(
    get_code_snippet_compexity,
    mode,
    code,
    complexity,
):
    """Ensures that cognitive complexity count is correct."""
    assert get_code_snippet_compexity(mode(code)) == complexity
