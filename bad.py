# -*- coding: utf-8 -*-
# 1, Space invaders!
# Credits: https://twitter.com/raymondh/status/1131103570856632321

x = 1
x -=- x
print(x)
# => 2

o = 2
o+=+o
print(o)
# => 4

print(3 --0-- 5 == 8)
# => True


# 2, The mistic dots
# Credits: https://stackoverflow.com/a/43487979/4842742

print(0..__eq__(0))
# => True

print(....__eq__(((...))))
# => True


# 3, Shredinger Return

def some_func():
    try:
        return 'from_try'
    finally:
        return 'from_finally'

some_func()
# => 'from_finally'


# 4, the C-ursed legacy
# Credits: https://twitter.com/dabeaz/status/1199376319961849861

a = [(0, 'Hello'), (1, 'world')]
for ['>']['>'>'>'], x in a:
    print(x)

# => Hello
# => world


# 5, Classes signed by the Black Sorcerer

class _:
    [(),...,()]#[(),...,()]
    _ = '_'

print(_._)  # this operator also looks familiar 🤔
# => '_'


# 6, Classes metamagic

class Example(type((lambda: 1)())):
    ...

print(Example(1) + Example(3))
# => 4


# 7, Regenerators

a = ['a', 'b']
print(set(x + '!' for x in a))
# => {'b!', 'a!'}

print(set((yield x + '!') for x in a))
# => {'b!', None, 'a!'}


# 8, Implicitly explicit emails
# Credits: https://twitter.com/raymondh/status/1186868472178806785

class G:
    def __init__(self, s):
        self.s = s
    def __getattr__(self, t):
        return G(self.s + '.' + str(t))
    def __rmatmul__(self, other):
        return other + '@' + self.s

username, example = 'username', G('example')
print(username@example.com)
# => username@example.com


# 9, Some strings are not what they seem

def main():
    """My name is {__file__}/{__name__}!"""

print(main().__doc__)
# => None

# Friendly reminder:
print(f"{getattr(__import__('os'), 'eman'[None:None:-1])}")
# => posix


# Links:
# https://github.com/satwikkansal/wtfpython
# https://github.com/sobolevn/python-code-disasters
# https://github.com/gahjelle/pythonji
