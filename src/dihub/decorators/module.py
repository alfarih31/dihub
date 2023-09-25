from typing import List, Any, Callable, Union

from dihub.__internal.helpers import AnnotationOf

from dihub.constants import _MODULE_ANNOTATIONS
from dihub.types import Value, Providers, Modules, ModuleAnnotation


def __get_list_defaults(arr: List[Any]) -> List[Any]:
    if arr is None:
        return []

    return arr


def __process_module_decorator(cls: Value, imports: Modules, providers: Providers) -> Value:
    AnnotationOf(cls).set(_MODULE_ANNOTATIONS, ModuleAnnotation(
        imports=__get_list_defaults(imports),
        providers=__get_list_defaults(providers)))

    return cls


def module(cls: Value = None, /, *, imports: Modules = None, providers: Providers = None) -> Union[Callable[[Value], Value], Value]:
    def wrapper(_cls: Value) -> Value:
        return __process_module_decorator(_cls, imports, providers)

    if cls is None:
        return wrapper

    return wrapper(cls)
