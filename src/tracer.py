import sys
from pprint import pprint

def dispatch_call(frame):
    # print(f"dispatch_call: {frame=}")
    pass

def dispatch_line(frame):
    # print(f"dispatch_line: {frame=}")
    pprint(f"{frame.f_lineno}: {frame.f_code.co_name}: {frame.f_locals}")
    pass

def dispatch_return(frame):
    pass

def dispatch_exception(frame):
    pass

def dispatch_opcode(frame):
    pass


def tracefunc(frame, event, arg):
    mapping = {
        "call": dispatch_call,
        "line": dispatch_line,
        "return": dispatch_return,
        "exception": dispatch_exception,
        "opcode": dispatch_opcode,
    }
    fn = mapping[event]

    # Trace each line, not just each call
    frame.f_trace = tracefunc
    frame.f_trace_lines = True
    frame.f_trace_opcodes = False
    fn(frame)

class TracerContextManager:
    def __enter__(self):
        sys.settrace(tracefunc)

    def __exit__(self, *exc):
        sys.settrace(None)

class Tracer:
    """namespace"""
    @staticmethod
    def trace_manager():
        return TracerContextManager()

class A:
    def __init__(self, x):
        self.x = x

    def __repr__(self) -> str:
        return f"A(x={getattr(self, 'x', None)})"

def fn():
    a = A(1)
    fn2()
    a = 1+1
    b = a + 1
    return b

def fn2():
    a = 3
    return a


with Tracer.trace_manager() as t:
    fn()
