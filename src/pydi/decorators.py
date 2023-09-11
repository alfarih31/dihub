from inspect import isfunction
from typing import Callable, List, Any, Protocol, Type

from pydi.__internal.delegates import ModuleDelegate, InjectedDelegate
from pydi.__internal.proxies import PrimitiveProxy
from pydi.constants import _MODULE_ANNOTATIONS, ProviderScope, _PROVIDER_ANNOTATIONS
from pydi.exceptions import NotAPyDIModule, AnnotationsNotSupported, NotAPyDIProvider
from pydi.types import InjectToken, Providers, Modules, Value, ModuleAnnotation, ProviderAnnotation, _Instance, IRootRunner, IModuleDelegate


def __get_list_defaults(arr: List[Any]) -> List[Any]:
    if arr is None:
        return []

    return arr


def module(imports: Modules = [], providers: Providers = []) -> Callable[[Value], Value]:
    def wrapped(cls: Value) -> Value:
        cls.__annotations__[_MODULE_ANNOTATIONS] = ModuleAnnotation(
            imports=__get_list_defaults(imports),
            providers=__get_list_defaults(providers))

        return cls

    return wrapped


def inject(token: InjectToken) -> InjectedDelegate:
    return InjectedDelegate(token)


class root(Protocol[Value]):
    __module_delegate: IModuleDelegate = None

    def __init__(self, decorated_class: Value):
        if decorated_class.__annotations__.get(_MODULE_ANNOTATIONS) is None:
            raise NotAPyDIModule(decorated_class.__name__)

        self.__module_delegate = ModuleDelegate(decorated_class, None)

    def __new__(cls, decorated_class: Value) -> Value:
        return super().__new__(cls)

    def __call__(self, *args, **kwargs) -> Type[Value]:
        self.__module_delegate.on_boot()
        self.__module_delegate.on_post_boot()

        base_module_instance = self.__module_delegate.base_module(*args, **kwargs)
        if isinstance(base_module_instance, IRootRunner):
            base_module_instance.after_boot(self.__module_delegate)

        return base_module_instance


def provider(token: InjectToken, scope: ProviderScope = ProviderScope.GLOBAL):
    def wrapper(provide: Value) -> Value:
        if isfunction(provide):
            provide = PrimitiveProxy(provide())

        provide.__annotations__[_PROVIDER_ANNOTATIONS] = ProviderAnnotation(token=token, scope=scope)
        return provide

    return wrapper


def export(provide: Value) -> Value:
    try:
        provider_annotations: ProviderAnnotation = provide.__annotations__.get(_PROVIDER_ANNOTATIONS)
        if provider_annotations is None:
            raise NotAPyDIProvider(str(provide))
        provide.__annotations__[_PROVIDER_ANNOTATIONS] = ProviderAnnotation(token=provider_annotations.token, scope=provider_annotations.scope,
                                                                            exported=True)
        return provide
    except TypeError:
        raise AnnotationsNotSupported(str(provide))


def for_root(m: _Instance) -> _Instance:
    module_annotations: ModuleAnnotation = m.__annotations__.get(_MODULE_ANNOTATIONS)
    if module_annotations is None:
        raise NotAPyDIModule(str(m))
    m.__annotations__[_MODULE_ANNOTATIONS] = ModuleAnnotation(imports=module_annotations.imports, providers=module_annotations.providers,
                                                              for_root=True)

    return m
