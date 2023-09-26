from typing import Any, Type, Optional

from dihub.exceptions import AnnotationsNotSupported
from dihub.types import Value, NOTABLE
from .class_helper import get_class_name


def is_primitive(obj):
    return not hasattr(obj, '__dict__')


class AnnotationOf:
    __source: NOTABLE

    def __init__(self, source: NOTABLE):
        self.__source = source

    def get(self, ann_name: str, metaclass: Optional[Type[Value]] = None) -> Optional[Value]:
        try:
            value = self.__source.__annotations__[ann_name]
            if metaclass is None:
                return value

            if not isinstance(value, metaclass):
                raise ValueError("The annotation values doesn't implement '%s'. Actual '%s'" % (
                    get_class_name(metaclass), get_class_name(value, True)))

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
