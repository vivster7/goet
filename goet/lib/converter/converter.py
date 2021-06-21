from collections import defaultdict
from collections.abc import Set
from base64 import b85encode
from datetime import datetime
from typing import Any, Union
from types import (
    BuiltinFunctionType,
    BuiltinMethodType,
    FunctionType,
    MethodType,
    LambdaType,
    ModuleType,
)

from cattr.converters import Converter, GenConverter, NoneType

from functools import partial
from textwrap import shorten


def is_function(obj):
    return isinstance(
        obj,
        (
            BuiltinFunctionType,
            BuiltinMethodType,
            FunctionType,
            MethodType,
            LambdaType,
            partial,
        ),
    )


def is_jsonable_primitive(typ: type) -> bool:
    return typ in (str, int, float, bool, type(None))


def is_jsonable_container(typ: type) -> bool:
    return typ in (list, tuple, dict, set, frozenset)


def is_jsonable(typ: type) -> bool:
    return is_jsonable_primitive(typ) or is_jsonable_container(typ)


def is_not_jsonable(obj: Any) -> bool:
    return not is_jsonable(obj)


def unstructure_complex_types(
    obj: Any,
    memo: dict,
) -> Union[str, int, float, bool, NoneType, list, dict]:
    # Handles recursive cases
    if is_jsonable_primitive(type(obj)):
        return obj

    obj_id = id(obj)
    if obj_id in memo:
        return f"<recursive {shorten(repr(obj), width=30, placeholder=' ...')}>"
    else:
        memo[obj_id] = True

    unknown_name = "<unknown>"
    if is_function(obj):
        name = getattr(obj, "__name__", unknown_name)
        return f"<function {name}>"
    elif isinstance(obj, ModuleType):
        return repr(obj)
    elif isinstance(obj, type):
        return repr(obj)
    elif hasattr(obj, "__slots__"):
        return {
            slot: unstructure_complex_types(getattr(obj, slot), memo)
            for slot in obj.__slots__
            if not slot.startswith("__")
        }
    elif hasattr(obj, "__dict__"):
        if isinstance(obj, type):
            return {obj.__name__: repr(obj)}
        return {
            k: unstructure_complex_types(v, memo)
            for k, v in obj.__dict__.items()
            if not k.startswith("__")
        }
    elif isinstance(obj, (dict, defaultdict)):
        return {
            k: unstructure_complex_types(v, memo)
            for k, v in obj.items()
            if not k.startswith("__")
        }
    elif hasattr(obj, "__iter__"):
        return [unstructure_complex_types(x, memo) for x in iter(obj)]
    else:
        # return {repr(obj): unknown_name}
        return {}


def configure_converter(converter: Converter):
    """
    Configure the converter for use with the stdlib json module.

    * bytes are serialized as base64 strings
    * datetimes are serialized as ISO 8601
    * counters are serialized as dicts
    * sets are serialized as lists
    """

    def unstructure_bytes(b: bytes) -> str:
        return (b85encode(b) if b else b"").decode("utf8")

    converter.register_unstructure_hook(bytes, unstructure_bytes)

    def unstructure_datetime(dt: datetime) -> str:
        return dt.isoformat()

    converter.register_unstructure_hook(datetime, unstructure_datetime)

    converter.register_unstructure_hook_func(
        is_not_jsonable, lambda o: unstructure_complex_types(o, {})
    )


def make_converter(*args, **kwargs) -> GenConverter:
    kwargs["unstruct_collection_overrides"] = {
        **kwargs.get("unstruct_collection_overrides", {}),
        Set: list,
        # Mapping: dict,
        # Counter: dict,
    }
    converter = GenConverter(*args, **kwargs)
    configure_converter(converter)

    return converter
