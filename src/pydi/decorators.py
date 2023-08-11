from inspect import isfunction
from typing import Callable, List, Any

from pydi.__internal.delegates import InjectedDelegate, ModuleDelegate
from pydi.__internal.proxies import PrimitiveProxy
from pydi.annotations import ModuleAnnotation, ProviderAnnotation
from pydi.constants import _MODULE_ANNOTATIONS, ProviderScope, _PROVIDER_ANNOTATIONS
from pydi.exceptions import NotAPyDIModule, AnnotationsNotSupported, NotAPyDIProvider
from pydi.typing import InjectToken
from pydi.typing import Providers, Modules, IModuleDelegate, Provide


def __get_list_defaults(arr: List[Any]) -> List[Any]:
    if arr is None:
        return []

    return arr


def module(imports: Modules = [], providers: Providers = []) -> Callable[[type], type]:
    def wrapped(cls: type) -> type:
        cls.__annotations__[_MODULE_ANNOTATIONS] = ModuleAnnotation(
            imports=__get_list_defaults(imports),
            providers=__get_list_defaults(providers))

        return cls

    return wrapped


def inject(token: InjectToken) -> InjectedDelegate:
    return InjectedDelegate(token)


def root(cls: type) -> IModuleDelegate:
    if cls.__annotations__.get(_MODULE_ANNOTATIONS) is None:
        raise NotAPyDIModule(cls.__name__)

    m = ModuleDelegate(cls, None)
    m.on_boot()
    m.on_post_boot()

    return m


def provider(token: InjectToken, scope: ProviderScope = ProviderScope.GLOBAL):
    def wrapper(provide: Provide) -> Provide:
        if isfunction(provide):
            provide = PrimitiveProxy(provide())

        provide.__annotations__[_PROVIDER_ANNOTATIONS] = ProviderAnnotation(token=token, scope=scope)
        return provide

    return wrapper


def export(provide: Provide) -> Provide:
    try:
        provider_annotations: ProviderAnnotation = provide.__annotations__.get(_PROVIDER_ANNOTATIONS)
        if provider_annotations is None:
            raise NotAPyDIProvider(str(provide))
        provide.__annotations__[_PROVIDER_ANNOTATIONS] = ProviderAnnotation(token=provider_annotations.token, scope=provider_annotations.scope,
                                                                            exported=True)
        return provide
    except TypeError:
        raise AnnotationsNotSupported(str(provide))
