
from collections import defaultdict
import json
from collections.abc import Set
from base64 import b85encode
from datetime import datetime
from typing import Any, Union

from cattr.converters import Converter, GenConverter


def is_jsonable(typ: type) -> bool:
    return typ in (str, int, float, bool, list, tuple, dict, type(None))

def is_not_jsonable(obj: Any) -> bool:
    return not is_jsonable(obj)

def unstructure_not_jsonable(obj: Any) -> Union[list, dict]:
    unknown_name = "<unknown>"
    if callable(obj):
        name = getattr(obj, '__name__', unknown_name)
        return {name: f"<function {name}>"}
    elif hasattr(obj, '__slots__'):
        return {slot: getattr(obj, slot) for slot in obj.__slots__ if not slot.startswith('__')}
    elif hasattr(obj, '__dict__'):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith('__')}
    elif isinstance(obj, defaultdict):
        return {k: v for k, v in obj.items()}
    elif hasattr(obj, '__iter__'):
        return list(iter(obj))
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


    converter.register_unstructure_hook_func(is_not_jsonable, unstructure_not_jsonable)


def make_converter(*args, **kwargs) -> GenConverter:
    kwargs["unstruct_collection_overrides"] = {
        **kwargs.get("unstruct_collection_overrides", {}),
        Set: list,
        # Counter: dict,
    }
    converter = GenConverter(*args, **kwargs)
    configure_converter(converter)

    return converter
