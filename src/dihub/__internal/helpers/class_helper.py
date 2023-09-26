from typing import Any

from dihub.types import InjectToken


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
