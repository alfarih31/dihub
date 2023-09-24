from typing import Any, Type, Optional

from pydi.exceptions import AnnotationsNotSupported
from pydi.types import Value, NOTABLE


def is_primitive(obj):
    return not hasattr(obj, '__dict__')


class AnnotationOf:
    __source: NOTABLE

    def __init__(self, source: NOTABLE):
        self.__source = source

    def get(self, ann_name: str, metaclass: Type[Value] = None) -> Optional[Value]:
        try:
            value = self.__source.__annotations__[ann_name]
            if metaclass is None:
                return value

            if not isinstance(value, metaclass):
                raise ValueError("The annotation values doesn't implement '%s'. Actual '%s'" % (
                    metaclass.__name__, value.__class__.__name__ if hasattr(value, "__class__") else type(value)))

            return value
        except AttributeError:
            raise AnnotationsNotSupported(str(self.__source))
        except KeyError:
            return None

    def set(self, ann_name: str, value: Any):
        try:
            self.__source.__annotations__[ann_name] = value
        except AttributeError:
            raise AnnotationsNotSupported(str(self.__source))
