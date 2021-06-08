from typing import Any, Dict, Optional, Tuple
from collections.abc import Callable

import attr
import cattr
from cattr.converters import Converter, GenConverter
from goet.lib.converter.converter import make_converter
import json
from hypothesis import strategies as st


st.register_type_strategy(Any, st.from_type(type).flatmap(st.from_type))
# st.register_type_strategy(object, lambda obj: repr(obj))
# st.register_type_strategy(bytes, lambda x: repr(x))
# st.register_type_strategy(Callable, lambda callable: repr(callable))


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
    # co_varnames: Tuple[str]
    # co_cellvars: Tuple[str]
    # co_freevars: Tuple[str]
    co_code: bytes
    # co_consts: Tuple[str, int, float, bool]
    # co_names: Tuple[str]
    co_filename: str
    co_firstlineno: int
    co_lnotab: bytes
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
            # co_varnames=syscode.co_varnames,
            # co_cellvars=syscode.co_cellvars,
            # co_freevars=syscode.co_freevars,
            co_code=syscode.co_code,
            # co_consts=syscode.co_consts,
            # co_names=syscode.co_names,
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
    # f_globals: Dict[str, Any]
    # f_builtins: Dict[str, Any]
    f_lasti: int
    f_trace: Optional[Callable]
    f_trace_lines: bool
    f_trace_opcodes: bool
    f_lineno: int

    @classmethod
    def from_sysframe(cls, sysframe):
        return cls(
            f_back=Frame.from_sysframe(sysframe.f_back) if sysframe.f_back else None,
            f_code=Code.from_syscode(sysframe.f_code),
            f_locals=sysframe.f_locals,
            # f_globals=sysframe.f_globals,
            # f_builtins=sysframe.f_builtins,
            f_lasti=sysframe.f_lasti,
            f_trace=sysframe.f_trace,
            f_trace_lines=sysframe.f_trace_lines,
            f_trace_opcodes=sysframe.f_trace_opcodes,
            f_lineno=sysframe.f_lineno,
        )
    
    def to_json(self):
        # import pickle
        # converter = GenConverter()
        # def unstructure_object(obj: Any) -> Any:
        #     try:
        #         return pickle.dumps(obj)
        #     except TypeError:
        #         print(f'{obj=} is not pickleable')
        #         return str(obj)

        # converter.register_unstructure_hook(Frame, converter.unstructure_attrs_asdict)
        # converter.register_unstructure_hook(Code, converter.unstructure_attrs_asdict)
        # converter.register_unstructure_hook(object, unstructure_object)

        # unstructured = converter.unstructure(self)
        # print(f"{unstructured=}")
        # return json.dumps(unstructured)

        converter = make_converter()
        unstructured = converter.unstructure(self)
        return json.dumps(unstructured)
        # first_pass = converter.unstructure(self)

        # def is_jsonable(obj):
        #     jsonable_types = (str, int, float, bool, list, tuple, dict, type(None))
        #     return isinstance(obj, jsonable_types)

        # def is_not_jsonable(obj):
        #     return not is_jsonable(obj)

        # def unstructure_not_jsonable(obj):
        #     for attr in dir(obj):
        #         if attr.startswith('__'):
        #             continue
        #         elif callable(obj.attr):
        #             return json.dumps({attr: repr(obj.attr)})
        #         elif is_jsonable(obj.attr):
        #             return json.dumps({attr: obj.attr})
        #         else:
        #             return unstructure_not_jsonable(obj.attr)

                

        # c2 = Converter()
        # c2.register_unstructure_hook_func(is_not_jsonable, unstructure_not_jsonable)
        # second_pass = c2.unstructure(first_pass)

        # return json.dumps(second_pass)


# Must be called after Frame is defined to resolve the `f_back: Frame` field.
attr.resolve_types(Frame, globals(), locals())

# from cattr.preconf.json import make_converter
# converter = make_converter()
# child = st.from_type(Frame).example()
# child.f_back = st.from_type(Frame).example()
# # child.f_code.co_code = b'123'
# print(json.dumps(converter.unstructure(child)))
# print(child == converter.structure(converter.unstructure(child), Frame))
