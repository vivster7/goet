import sys
from pprint import pprint
from typing import Any, Callable, Dict, Literal, Optional, Tuple

import attr
import cattr
from hypothesis import strategies as st

Event = (
    Literal["call"]
    | Literal["line"]
    | Literal["return"]
    | Literal["exception"]
    | Literal["opcode"]
)
st.register_type_strategy(Any, st.from_type(type).flatmap(st.from_type))


@attr.resolve_types
@attr.define
class Code:
    """Code objects represent byte-compiled executable Python code, or bytecode.

    The difference between a code object and a function object is that the function object contains an explicit reference to the
    function’s globals (the module in which it was defined), while a code object contains no context; also the default argument
    values are stored in the function object, not in the code object (because they represent values calculated at run-time).
    Unlike function objects, code objects are immutable and contain no references (directly or indirectly) to mutable objects.

    Special read-only attributes:
        co_name gives the function name
        co_argcount is the total number of positional arguments (including positional-only arguments and arguments with default values)
        co_posonlyargcount is the number of positional-only arguments (including arguments with default values)
        co_kwonlyargcount is the number of keyword-only arguments (including arguments with default values)
        co_nlocals is the number of local variables used by the function (including arguments)
        co_varnames is a tuple containing the names of the local variables (starting with the argument names)
        co_cellvars is a tuple containing the names of local variables that are referenced by nested functions
        co_freevars is a tuple containing the names of free variables
        co_code is a string representing the sequence of bytecode instructions
        co_consts is a tuple containing the literals used by the bytecode
        co_names is a tuple containing the names used by the bytecode
        co_filename is the filename from which the code was compiled
        co_firstlineno is the first line number of the function
        co_lnotab is a string encoding the mapping from bytecode offsets to line numbers (for details see the source code of the interpreter)
        co_stacksize is the required stack size
        co_flags is an integer encoding a number of flags for the interpreter.

    The following flag bits are defined for co_flags: bit 0x04 is set if the function uses the *arguments syntax to accept an arbitrary number of positional arguments
        bit 0x08 is set if the function uses the **keywords syntax to accept arbitrary keyword arguments
        bit 0x20 is set if the function is a generator.

    Future feature declarations (from __future__ import division) also use bits in co_flags to indicate whether a code object was compiled with a particular feature enabled: bit 0x2000 is set if the function was compiled with future division enabled
        bits 0x10 and 0x1000 were used in earlier versions of Python.

    Other bits in co_flags are reserved for internal use.

    If a code object represents a function, the first item in co_consts is the documentation string of the function, or None if undefined.
    """

    co_name: str
    co_argcount: int
    co_posonlyargcount: int
    co_kwonlyargcount: int
    co_nlocals: int
    co_varnames: Tuple[str]
    co_cellvars: Tuple[str]
    co_freevars: Tuple[str]
    co_code: str
    co_consts: Tuple[str]  # int, float, bool]
    co_names: Tuple[str]
    co_filename: str
    co_firstlineno: int
    co_lnotab: str
    co_stacksize: int
    co_flags: int

    @classmethod
    def from_syscode(cls, syscode):
        return cls(
            co_name=syscode.co_name,
            co_argcount=syscode.co_argcount,
            co_posonlyargcount=syscode.co_posonlyargcount,
            co_kwonlyargcount=syscode.co_kwonlyargcount,
            co_nlocals=syscode.co_nlocals,
            co_varnames=syscode.co_varnames,
            co_cellvars=syscode.co_cellvars,
            co_freevars=syscode.co_freevars,
            co_code=syscode.co_code,
            co_consts=syscode.co_consts,
            co_names=syscode.co_names,
            co_filename=syscode.co_filename,
            co_firstlineno=syscode.co_firstlineno,
            co_lnotab=syscode.co_lnotab,
            co_stacksize=syscode.co_stacksize,
            co_flags=syscode.co_flags,
        )


@attr.define
class Frame:
    """Frame objects represent execution frames. They may occur in traceback objects (see below), and are also passed to registered trace functions.

    Special read-only attributes:
        f_back is to the previous stack frame (towards the caller), or None if this is the bottom stack frame
        f_code is the code object being executed in this frame
        f_locals is the dictionary used to look up local variables
        f_globals is used for global variables
        f_builtins is used for built-in (intrinsic) names
        f_lasti gives the precise instruction (this is an index into the bytecode string of the code object).

    Special writable attributes:
        f_trace, if not None, is a function called for various events during code execution (this is used by the debugger).
        Normally an event is triggered for each new source line - this can be disabled by setting f_trace_lines to False.

    Implementations may allow per-opcode events to be requested by setting f_trace_opcodes to True.
    Note that this may lead to undefined interpreter behaviour if exceptions raised by the trace function escape to the function being traced.

    f_lineno is the current line number of the frame — writing to this from within a trace function jumps to the given line (only for the bottom-most frame).
    A debugger can implement a Jump command (aka Set Next Statement) by writing to f_lineno.
    """

    f_back: Optional["Frame"]
    f_code: Code
    f_locals: Dict[str, Any]
    f_globals: Dict[str, Any]
    f_builtins: Dict[str, Any]
    f_lasti: int
    f_trace: Optional[Callable]
    f_trace_lines: bool
    f_trace_opcodes: bool
    f_lineno: int

    @classmethod
    def from_sysframe(cls, sysframe):
        return cls(
            f_back=sysframe.f_back,
            f_code=sysframe.f_code,
            f_locals=sysframe.f_locals,
            f_globals=sysframe.f_globals,
            f_builtins=sysframe.f_builtins,
            f_lasti=sysframe.f_lasti,
            f_trace=sysframe.f_trace,
            f_trace_lines=sysframe.f_trace_lines,
            f_trace_opcodes=sysframe.f_trace_opcodes,
            f_lineno=sysframe.f_lineno,
        )


# Must be called after Frame is defined to resolve the `f_back: Frame` field.
attr.resolve_types(Frame, globals(), locals())

converter = cattr.GenConverter()

child = st.from_type(Frame).example()

pprint(child)
pprint(child == converter.structure(converter.unstructure(child), Frame))


class Tracer:
    """Tracer is used to record Python runtime.

    >>> with Tracer.trace_manager() as t:
    ...     fn()
    """

    def __init__(self):
        self.data = {}

    def __enter__(self):
        sys.settrace(self.tracefunc)

    def __exit__(self, *exc):
        sys.settrace(None)

    def dispatch_call(self, frame):
        # print(f"dispatch_call: {frame=}")
        pass

    def dispatch_line(self, frame):
        # print(f"dispatch_line: {frame=}")
        pprint(f"{frame.f_lineno}: {frame.f_code.co_name}: {frame.f_locals}: {frame}")
        # pprint(pickle.dumps(frame))
        pass

    def dispatch_return(self, frame):
        pass

    def dispatch_exception(self, frame):
        pass

    def dispatch_opcode(self, frame):
        pass

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


class A:
    def __init__(self, x):
        self.x = x

    def __repr__(self) -> str:
        return f"A(x={getattr(self, 'x', None)})"


def fn():
    a = A(1)
    fn2()
    a = 1 + 1
    b = a + 1
    return b


def fn2():
    a = 3
    return a


# with Tracer() as t:
#     fn()
