from inspect import getmembers
from typing import Optional, Self, Any, Tuple, List

from pydi.__internal.proxies import ProviderProxy
from pydi.constants import _MODULE_ANNOTATIONS, ProviderScope
from pydi.exceptions import (
    NotAPyDIModule,
    CannotResolveDependency,
    ModuleNotFound,
    ProviderNotFound,
)
from pydi.types import (
    InjectToken,
    IModuleDelegate,
    IProviderDelegate,
    ModuleAnnotation,
    ProviderAnnotation,
)
from .injected_delegate import InjectedDelegate
from .provider_delegate import ProviderDelegate


class ModuleDelegate(IModuleDelegate):
    __base_module: type
    __providers: ProviderDelegate
    __imported_modules_delegate: List[IModuleDelegate]
    __root_delegate: Self
    __for_root_imports: List[IModuleDelegate]

    def __init__(self, module: type, root_delegate: Optional[Self]):
        self.__base_module = module

        annotations: Optional[ModuleAnnotation] = module.__annotations__.get(
            _MODULE_ANNOTATIONS
        )
        if annotations is None:
            raise NotAPyDIModule(module.__str__())

        self.__root_delegate = root_delegate
        self.__providers = ProviderDelegate(annotations.providers)
        self.__imported_modules_delegate = [ModuleDelegate(m, self) for m in annotations.imports]

        self.__for_root_imports = []
        for md in self.__imported_modules_delegate:
            md_annotations: ModuleAnnotation = md.base_module.__annotations__.get(_MODULE_ANNOTATIONS)
            if md_annotations.for_root:
                self.__for_root_imports.append(md)

    @property
    def is_root(self) -> bool:
        return self.__root_delegate is None

    def __call__(self, *args, **kwargs):
        return self

    def __str__(self):
        imports_str = []
        for i in self.__imported_modules_delegate:
            imports_str.append(i.__str__())
        return "<%s%s<imports [%s]>>" % (
            self.__repr__(),
            str(self.__base_module),
            ",\n".join(imports_str),
        )

    def __eq__(self, other: Any):
        if isinstance(other, ModuleDelegate):
            return self.__base_module == other.__base_module
        elif isinstance(other, type):
            return self.__base_module == other

        return False

    def deep_eq(self, other: Any) -> bool:
        if not self.__eq__(other):
            return False
        return id(other) == id(self)

    def __getitem__(self, module: type) -> IModuleDelegate:
        for m in self.__imported_modules_delegate:
            if m == module:
                return m
        raise ModuleNotFound(module)

    def get_exported_provider(
            self, token: InjectToken
    ) -> Tuple[Optional[ProviderProxy], Optional[ProviderAnnotation]]:
        provider, annotations = self.__providers[token]
        if provider is not None and annotations.exported:
            if annotations.scope == ProviderScope.MODULE:
                return provider.__copy__(), annotations

            return provider, annotations

    def get_for_root_provider(self, token: InjectToken) -> Tuple[Optional[ProviderProxy], Optional[ProviderAnnotation]]:
        for rmd in self.__for_root_imports:
            try:
                dependency, annotations = rmd.get_exported_provider(token)
                return dependency, annotations
            except ProviderNotFound:
                continue

        if self.root_delegate is None:
            raise ProviderNotFound(token)

        return self.root_delegate.get_for_root_provider(token)

    def __resolve_providers_dependencies(self):
        for provider, _ in self.__providers:
            for dependency_name, injected_dependency in getmembers(
                    provider.provide, predicate=lambda x: isinstance(x, InjectedDelegate)
            ):
                dependency: Optional[ProviderProxy] = None
                annotations: Optional[ProviderAnnotation] = None
                # Resolve from self
                try:
                    dependency, annotations = self.__providers[
                        injected_dependency.token
                    ]
                except ProviderNotFound:
                    pass

                if dependency is None:
                    for m in self.__imported_modules_delegate:
                        try:
                            dependency, annotations = m.get_exported_provider(
                                injected_dependency.token
                            )
                            break
                        except ProviderNotFound:
                            continue

                if dependency is None:
                    try:
                        dependency, annotations = self.root_delegate.get_for_root_provider(injected_dependency.token)
                    except ProviderNotFound:
                        raise CannotResolveDependency(dependency_name, str(provider))

                # Decide how the dependency is resolved
                if annotations.scope == ProviderScope.LOCAL:
                    # Make the dependency uniqueness by copy
                    dependency = dependency.__copy__()
                else:
                    self.__providers.append(dependency)

                setattr(provider.provide, dependency_name, dependency)

    def __clean_up(self):
        # Delete all LOCAL scoped providers
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

    @property
    def providers(self) -> IProviderDelegate:
        return self.__providers

    @property
    def base_module(self) -> type:
        return self.__base_module

    @property
    def root_delegate(self) -> Self:
        return self.__root_delegate

    @property
    def for_root_imports(self) -> List[Self]:
        return self.__for_root_imports
