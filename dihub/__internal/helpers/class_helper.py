from inspect import getmembers
from typing import Any, List, Tuple, get_type_hints

from dihub.types import InjectToken, IInjectedDelegate


def get_class_name(obj: Any, class_first=False) -> str:
    if class_first:
        if hasattr(obj, '__class__'):
            return obj.__class__.__name__
        elif hasattr(obj, '__name__'):
            return obj.__name__
    else:
        if hasattr(obj, '__name__'):
            return obj.__name__
        elif hasattr(obj, '__class__'):
            return obj.__class__.__name__

    return type(obj).__name__


def get_inject_token_str(token: InjectToken) -> str:
    if isinstance(token, str):
        return token
    return get_class_name(token)


def discover_injected_delegate(cls: Any) -> List[Tuple[str, Any]]:
    members = {}
    for attr_name, attr_value in getmembers(cls, predicate=lambda x: isinstance(x, IInjectedDelegate)):
        members[attr_name] = attr_value

    for k, v in get_type_hints(cls, include_extras=True).items():
        if k not in members:
            if hasattr(v, "__metadata__"):
                for v_metadata in v.__metadata__:
                    if isinstance(v_metadata, IInjectedDelegate):
                        members[k] = v_metadata
                        break

    return [(k, v) for k, v in members.items()]
