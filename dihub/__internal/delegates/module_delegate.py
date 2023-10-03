from typing import Optional, Self, Any, Tuple, List

from dihub.__internal.helpers import (
    AnnotationOf,
    validate_dihub_module,
    get_class_name,
    discover_injected_delegate
)
from dihub.__internal.proxies import ProviderProxy
from dihub.constants import _MODULE_ANNOTATIONS, ProviderScope, ROOT_MODULE_DELEGATE
from dihub.exceptions import (
    CannotResolveDependency,
    ModuleNotFound,
    ProviderNotFound,
)
from dihub.types import (
    IModuleDelegate,
    IProviderDelegate,
    ModuleAnnotation,
    ProviderAnnotation,
    Instance,
)
from .injected_delegate import InjectedDelegate
from .provider_delegate import ProviderDelegate


class ModuleDelegate(IModuleDelegate):
    __base_class: type
    __providers: ProviderDelegate
    __imported_modules_delegate: List[IModuleDelegate]
    __parent_delegate: Self
    __for_root_imports: List[IModuleDelegate]

    def __init__(self, module: type, parent_delegate: Optional[Self]):
        validate_dihub_module(module)

        annotations = AnnotationOf(module).get(
            _MODULE_ANNOTATIONS, ModuleAnnotation
        )

        self.__base_class = module
        self.__parent_delegate = parent_delegate
        self.__providers = ProviderDelegate(annotations.providers)
        self.__imported_modules_delegate = [ModuleDelegate(m, self) for m in annotations.imports]

        self.__for_root_imports = []
        for md in self.__imported_modules_delegate:
            md_annotations = AnnotationOf(md.base_class).get(_MODULE_ANNOTATIONS, ModuleAnnotation)
            if md_annotations.for_root:
                self.__for_root_imports.append(md)

    @property
    def is_root(self) -> bool:
        return self.__parent_delegate is None

    def __call__(self, *args, **kwargs):
        return self

    def __str__(self):
        imports_str = []
        for i in self.__imported_modules_delegate:
            imports_str.append(get_class_name(i))
        return "<%s %s<imports [%s]>>" % (
            ModuleDelegate.__name__,
            get_class_name(self.__base_class),
            ",\n".join(imports_str),
        )

    def __eq__(self, other: Any):
        if isinstance(other, ModuleDelegate):
            return self.__base_class == other.__base_class
        elif isinstance(other, type):
            return self.__base_class == other

        return False

    def __setattr__(self, key, value):
        super(ModuleDelegate, self).__setattr__(key, value)
        setattr(self.__base_class, key, value)

    def deep_eq(self, other: Any) -> bool:
        if not self.__eq__(other):
            return False
        return id(other) == id(self)

    def __getitem__(self, module: Instance) -> IModuleDelegate:
        for m in self.__imported_modules_delegate:
            if m == module:
                return m
        raise ModuleNotFound(module)

    def get_exported_provider(
            self, token: str
    ) -> Tuple[Optional[ProviderProxy], Optional[ProviderAnnotation]]:
        provider, annotations = self.__providers[token]
        if provider is not None and annotations.exported:
            if annotations.scope == ProviderScope.MODULE:
                return provider.__copy__(), annotations

            return provider, annotations

        raise ProviderNotFound(token)

    def get_for_root_provider(self, token: str) -> Tuple[Optional[ProviderProxy], Optional[ProviderAnnotation]]:
        for rmd in self.__for_root_imports:
            try:
                dependency, annotations = rmd.get_exported_provider(token)
                return dependency, annotations
            except ProviderNotFound:
                continue

        if self.parent_delegate is None:
            """
                it's already on root
                Search from root providers. It's special ability for root module that
                all of the root exported providers can be accessed by the importd module providers 
            """
            return self.get_exported_provider(token)

        return self.parent_delegate.get_for_root_provider(token)

    def __resolve_providers_dependencies(self):
        def resolve_root_module_delegate(provider: ProviderProxy, attribute_name: str, injected_delegate: InjectedDelegate) -> bool:
            if injected_delegate.token == ROOT_MODULE_DELEGATE:
                setattr(provider.provide, attribute_name, self.root_delegate)

                return True

            return False

        for provider, _ in self.__providers:
            for dependency_name, injected_dependency in discover_injected_delegate(provider.provide):
                if resolve_root_module_delegate(provider, dependency_name, injected_dependency):
                    continue

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

                if not self.is_root and dependency is None:
                    try:
                        dependency, annotations = self.parent_delegate.get_for_root_provider(injected_dependency.token)
                    except ProviderNotFound:
                        raise CannotResolveDependency(dependency_name, str(provider))

                if dependency is None or annotations is None:
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
        self.__providers.on_boot()

        # Recursive boot imported module
        for i in self.__imported_modules_delegate:
            i.on_boot()

        # Injecting
        self.__resolve_providers_dependencies()

    def on_post_boot(self):
        self.__providers.on_post_boot()

        for i in self.__imported_modules_delegate:
            i.on_post_boot()

        self.__clean_up()

    @property
    def providers(self) -> IProviderDelegate:
        return self.__providers

    @property
    def base_class(self) -> type:
        return self.__base_class

    @property
    def root_delegate(self) -> Self:
        if not self.is_root:
            return self.parent_delegate.root_delegate

        return self

    @property
    def parent_delegate(self) -> Self:
        return self.__parent_delegate

    @property
    def imports(self) -> List[Self]:
        return self.__imported_modules_delegate
