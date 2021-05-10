import abc
from enum import Enum, unique
import sys
from typing import Literal, Protocol, Union
from goet.frame import Frame

Event = Union[Literal["call"], Literal["line"], Literal["return"], Literal["exception"], Literal["opcode"]]


class Tracer(Protocol):
    def dispatch_call(self, frame: Frame):
        raise NotImplementedError

    def dispatch_line(self, frame: Frame):
        raise NotImplementedError

    def dispatch_return(self, frame: Frame):
        raise NotImplementedError

    def dispatch_exception(self, frame: Frame):
        raise NotImplementedError

    def dispatch_opcode(self, frame: Frame):
        raise NotImplementedError    


class BaseTracer(abc.ABC, Tracer):
    """Tracer is used to record Python runtime."""

    def __enter__(self):
        sys.settrace(self.tracefunc)

    def __exit__(self, *exc):
        sys.settrace(None)

    def tracefunc(self, frame: Frame, event: Event, arg):
        mapping = {
            "call": self.dispatch_call,
            "line": self.dispatch_line,
            "return": self.dispatch_return,
            "exception": self.dispatch_exception,
            "opcode": self.dispatch_opcode,
        }
        fn = mapping[event]

        # Trace each line, not just each call
        frame.f_trace = self.tracefunc
        frame.f_trace_lines = True
        frame.f_trace_opcodes = False
        fn(frame)
