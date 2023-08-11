from inspect import getmembers
from typing import Optional, Self, Any, Tuple, Union, List

from pydi.__internal.delegates.provider_delegate import ProviderDelegate
from pydi.__internal.proxies.provider_proxy import ProviderProxy
from pydi.annotations import ModuleAnnotation, ProviderAnnotation
from pydi.constants import _MODULE_ANNOTATIONS, ProviderScope
from pydi.exceptions import NotAPyDIModule, CannotResolveDependency
from pydi.typing import InjectToken, IModuleDelegate
from .injected_delegate import InjectedDelegate


class ModuleDelegate(IModuleDelegate):
    __base_module: type
    __providers: ProviderDelegate
    __imported_providers: ProviderDelegate
    __imported_modules_delegate: List[Self]
    __root_delegate: Self

    def __init__(self, module: type, root_delegate: Optional[Self]):
        self.__base_module = module

        annotations: Optional[ModuleAnnotation] = module.__annotations__.get(_MODULE_ANNOTATIONS)
        if annotations is None:
            raise NotAPyDIModule(module.__str__())

        self.__root_delegate = root_delegate
        self.__providers = ProviderDelegate(annotations.providers)
        self.__imported_modules_delegate = [ModuleDelegate(m, root_delegate if not self.is_root else self) for m in annotations.imports]

    @property
    def is_root(self) -> bool:
        return self.__root_delegate is None

    def __call__(self, *args, **kwargs):
        return self

    def __str__(self):
        return "<%s %s>" % (self.__repr__(), str(self.__base_module))

    def __eq__(self, other: Any):
        if isinstance(other, ModuleDelegate):
            return self.__base_module == other.__base_module
        elif isinstance(other, type):
            return self.__base_module == other

        return False

    def __getitem__(self, attr: Tuple[Union[type, Self], InjectToken]) -> Optional[ProviderProxy]:
        if self.__eq__(attr[0]):
            provider, annotations = self.__providers[attr[1]]
            if provider is not None:
                return provider

        for m in self.__imported_modules_delegate:
            provider = m[attr]
            if provider is not None:
                return provider

    def __export_providers(self) -> ProviderDelegate:
        provider_delegate = ProviderDelegate([])
        for provider, annotations in self.__providers:
            if annotations.exported:
                if annotations.scope == ProviderScope.MODULE:
                    provider_delegate.append(provider.__copy__())
                    continue
                provider_delegate.append(provider)

        return provider_delegate

    def __export_provider(self, token: InjectToken) -> Tuple[Optional[ProviderProxy], Optional[ProviderAnnotation]]:
        provider, annotations = self.__providers[token]
        if provider is not None and annotations.exported:
            if annotations.scope == ProviderScope.MODULE:
                return provider.__copy__(), annotations

            return provider, annotations

    def __resolve_providers_dependencies(self):
        for provider, _ in self.__providers:
            for dependency_name, injected_dependency in getmembers(provider.provide, predicate=lambda x: isinstance(x, InjectedDelegate)):
                dependency: Optional[ProviderProxy]
                annotations: Optional[ProviderAnnotation]
                # Resolve from self
                dependency, annotations = self.__providers[injected_dependency.token]

                if dependency is None:
                    for m in self.__imported_modules_delegate:
                        dependency, annotations = m.__export_provider(injected_dependency.token)
                        if dependency is not None:
                            break

                if dependency is None:
                    dependency, annotations = self.__root_delegate.__providers[injected_dependency.token]

                if dependency is None:
                    raise CannotResolveDependency(dependency_name, str(provider))

                # Decide how the dependency is resolved
                if annotations.scope == ProviderScope.LOCAL:
                    dependency = dependency.__copy__()

                if annotations.scope == ProviderScope.MODULE:
                    self.__providers.append(dependency)

                setattr(provider.provide, dependency_name, dependency)

    def __clean_up(self):
        for p, annotations in self.__providers:
            if annotations.scope == ProviderScope.LOCAL:
                del self.__providers[annotations.token]

    def on_boot(self):
        # Recursive boot imported module
        for i in self.__imported_modules_delegate:
            i.on_boot()

        self.__providers.on_boot()

        # Injecting
        self.__resolve_providers_dependencies()

    def on_post_boot(self):
        for i in self.__imported_modules_delegate:
            i.on_post_boot()

        self.__providers.on_post_boot()

        self.__clean_up()
