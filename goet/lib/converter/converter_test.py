import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

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
test(float("infinity"), "Infinity")
test(float("-infinity"), "-Infinity")
test(float("NaN"), "NaN")
test(True, "true")
test(False, "false")
test(None, "null")
test("a", '"a"')

# Containers[Primitives]
test((), "[]")
test([], "[]")
test(set(), "[]")
test(frozenset(), "[]")
test({}, "{}")
test({"a": 1}, '{"a": 1}')
test(Counter(), "{}")
test(defaultdict(), "{}")

# Bytes
test(b"123", '"F)}j"')

# Datetimes
test(datetime(1, 2, 3, 4, 5, 6, 7), '"0001-02-03T04:05:06.000007"')

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
    y: Dict[str, Any]


test(C(x=1, y={"a": 1}), '{"x": 1, "y": {"a": 1}}')


@attr.frozen
class D:
    x: int


test(D(x=1), '{"x": 1}')


@dataclass
class E:
    x: int


test(E(x=1), '{"x": 1}')


class F:
    def __init__(self, f):
        self.f = f


test(F(f=F(f=None)), json.dumps({"f": {"f": None}}))

# Recursive class
ff = F(f=None)
ff.f = ff
test(ff, '{"f": "<recursive <__main__.F object at ...>"}')

# Functions
def f():
    return


test(f, '"<function f>"')


def g():
    return f


test(g, '"<function g>"')


def h(x):
    return x


test(h, '"<function h>"')


def i():
    return i


test(i, '"<function i>"')

test(lambda: 1, '"<function <lambda>>"')

# Containers[Complex]
test({"a": {"b": b"123"}}, '{"a": {"b": "F)}j"}}')
test({"a": {"f": f}}, '{"a": {"f": "<function f>"}}')
test({"a": {"A": A}}, '{"a": {"A": "<class \'__main__.A\'>"}}')
test({"a": {"b": B(x=1)}}, '{"a": {"b": {"x": 1}}}')
