# Copied from `flake8-quotes`
# https://github.com/zheller/flake8-quotes

# Original license

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import tokenize
from typing import Final
from collections.abc import Sequence

# I don't think this is a minimized state machine, but it's clearer this
# way. Namely, the class vs. function states can be merged

# In the start of the module when we're expecting possibly a string that gets marked as a docstring
STATE_EXPECT_MODULE_DOCSTRING: Final = 0
# After seeing the class keyword, we're waiting for the block colon (and do bracket counting)
STATE_EXPECT_CLASS_COLON: Final = 1
# After seeing the colon in a class definition we're expecting possibly a docstring
STATE_EXPECT_CLASS_DOCSTRING: Final = 2
# Same as EXPECT_CLASS_COLON, but for function definitions
STATE_EXPECT_FUNCTION_COLON: Final = 3
# Same as EXPECT_CLASS_DOCSTRING, but for function definitions
STATE_EXPECT_FUNCTION_DOCSTRING: Final = 4
# Just skipping tokens until we observe a class or a def.
STATE_OTHER: Final = 5

# These tokens don't matter here - they don't get in the way of docstrings
TOKENS_TO_IGNORE: Final = (
    tokenize.NEWLINE,
    tokenize.INDENT,
    tokenize.DEDENT,
    tokenize.NL,
    tokenize.COMMENT,
)


def get_docstring_tokens(
    tokens: Sequence[tokenize.TokenInfo],
) -> set[tokenize.TokenInfo]:
    """Return tokens that represent docstrings."""
    state = STATE_EXPECT_MODULE_DOCSTRING
    # The number of currently open parentheses, square brackets, etc.
    # This doesn't check if they're properly balanced, i.e. there isn't ([)], but we shouldn't
    # need to - if they aren't, it shouldn't parse at all, so we ignore the bracket type
    bracket_count = 0
    docstring_tokens = set()

    for token in tokens:
        if token.type in TOKENS_TO_IGNORE:
            continue
        if token.type == tokenize.STRING:
            if state in [
                STATE_EXPECT_MODULE_DOCSTRING,
                STATE_EXPECT_CLASS_DOCSTRING,
                STATE_EXPECT_FUNCTION_DOCSTRING,
            ]:
                docstring_tokens.add(token)
                state = STATE_OTHER
        # A class means we'll expect the class token
        elif token.type == tokenize.NAME and token.string == 'class':
            state = STATE_EXPECT_CLASS_COLON
            # Just in case - they should be balanced normally
            bracket_count = 0
        # A def means we'll expect a colon after that
        elif token.type == tokenize.NAME and token.string == 'def':
            state = STATE_EXPECT_FUNCTION_COLON
            # Just in case - they should be balanced normally
            bracket_count = 0
        # If we get a colon and we're expecting it, move to the next state
        elif token.type == tokenize.OP and token.string == ':':
            # If there are still left brackets open, it must be something other than the block start
            if bracket_count == 0:
                if state == STATE_EXPECT_CLASS_COLON:
                    state = STATE_EXPECT_CLASS_DOCSTRING
                elif state == STATE_EXPECT_FUNCTION_COLON:
                    state = STATE_EXPECT_FUNCTION_DOCSTRING
        # Count opening and closing brackets in bracket_count
        elif token.type == tokenize.OP and token.string in ['(', '[', '{']:
            bracket_count += 1
            if state in [
                STATE_EXPECT_MODULE_DOCSTRING,
                STATE_EXPECT_CLASS_DOCSTRING,
                STATE_EXPECT_FUNCTION_DOCSTRING,
            ]:
                state = STATE_OTHER
        elif token.type == tokenize.OP and token.string in [')', ']', '}']:
            bracket_count -= 1
            if state in [
                STATE_EXPECT_MODULE_DOCSTRING,
                STATE_EXPECT_CLASS_DOCSTRING,
                STATE_EXPECT_FUNCTION_DOCSTRING,
            ]:
                state = STATE_OTHER
        # The token is not one of the recognized types. If we're expecting a colon, then all good,
        # but if we're expecting a docstring, it would no longer be a docstring
        elif state in [
            STATE_EXPECT_MODULE_DOCSTRING,
            STATE_EXPECT_CLASS_DOCSTRING,
            STATE_EXPECT_FUNCTION_DOCSTRING,
        ]:
            state = STATE_OTHER

    return docstring_tokens
