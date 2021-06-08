import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import attr
from goet.lib.converter.converter import make_converter

converter = make_converter()


def test(x: Any, y: Any) -> None:
    try:
        val = json.dumps(converter.unstructure(x))
        assert val == y
    except AssertionError as e:
        print(f"{val} != {y}")

## Primitives
test(1, "1")
test(0, "0")
test(-1, "-1")
test(3.13, "3.13")
test(1e100, "1e+100")
test(1e-100, "1e-100")
test(float('infinity'), "Infinity")
test(float('-infinity'), "-Infinity")
test(float('NaN'), "NaN")
test(True, "true")
test(False, "false")
test("a", "\"a\"")

# Containers
test((), "[]")
test([], "[]")
test(set(), "[]")
test(frozenset(), "[]")
test({}, "{}")
test(Counter(), "{}")
test(defaultdict(), "{}")

# Bytes
test(b'123', "\"F)}j\"")

# Datetimes
test(datetime(1,2,3,4,5,6,7), "\"0001-02-03T04:05:06.000007\"")

# Custom classes
test(object(), "{}")

class A:
    pass
test(A(), "{}")

class B:
    def __init__(self, x):
        self.x = x
test(B(x=1), '{"x": 1}')

@attr.define
class C:
    x: int
test(C(x=1), '{"x": 1}')

@attr.frozen
class D:
    x: int
test(D(x=1), '{"x": 1}')

@dataclass
class E:
    x: int
test(E(x=1), '{"x": 1}')

# Functions
def f():
    return
test(f, '{"f": "<function f>"}')

def g():
    return f
test(g, '{"g": "<function g>"}')    

def h(x):
    return x
test(h, '{"h": "<function h>"}')

def i():
    return i
test(i, '{"i": "<function i>"}')

test(lambda: 1, '{"<lambda>": "<function <lambda>>"}')
