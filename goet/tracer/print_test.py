from goet.lib.frame.frame import Frame
import sys
from goet.tracer.print import PrintTracer


class A:
    def __init__(self, x):
        self.x = x

    def __repr__(self) -> str:
        return f"A(x={getattr(self, 'x', None)})"


def fn():
    a = A(1)

    def f3():
        return a

    fn2()
    f3()
    a = 1 + 1
    b = a + 1
    return b


def fn2():
    a = 3
    return a


# from pprint import pprint
# import json
# import ipdb; ipdb.set_trace()
# frame = Frame.from_sysframe(sys._getframe(), 1, 1)
# pprint(json.loads(frame.to_json()), indent=4)

with PrintTracer() as t:
    fn()
