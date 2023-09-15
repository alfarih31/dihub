from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TypeAlias, TypeVar, Callable, List, Union, Self, Tuple, Optional, Any, Type

from .constants import ProviderScope

_Instance = TypeVar('_Instance', bound=type, covariant=True)
Value = TypeVar("Value", covariant=True)
Method: TypeAlias = Callable[[_Instance], Value]

InjectToken = Union[str, type]

_as_class: TypeAlias = type
_as_primitive: TypeAlias = Union[str, int, bool, float]

Provide = TypeVar("Provide", covariant=True)

Modules: TypeAlias = List[type]


class IProviderProxy(ABC):
    @abstractmethod
    def on_boot(self): ...

    @abstractmethod
    def on_post_boot(self): ...

    @abstractmethod
    def deep_eq(self, other: Any) -> bool: ...

    @abstractmethod
    def cast(self, metaclass: Type[Value]) -> Value: ...

    @abstractmethod
    def release(self) -> Value: ...


Providers: TypeAlias = List[Provide]


@dataclass(frozen=True)
class ProviderAnnotation:
    token: str
    scope: ProviderScope
    exported: bool = False


class IProviderDelegate(ABC):
    @abstractmethod
    def __getitem__(self, token: InjectToken) -> Tuple[IProviderProxy, ProviderAnnotation]: ...


class IModuleDelegate(ABC):
    @abstractmethod
    def __getitem__(self, module: type) -> Self: ...

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Self: ...

    @abstractmethod
    def deep_eq(self, other: Any) -> bool: ...

    @property
    @abstractmethod
    def providers(self) -> IProviderDelegate: ...

    @property
    @abstractmethod
    def for_root_imports(self) -> List[Self]: ...

    @property
    @abstractmethod
    def base_class(self) -> type: ...

    @property
    @abstractmethod
    def root_delegate(self) -> Self: ...

    @abstractmethod
    def on_boot(self): ...

    @abstractmethod
    def on_post_boot(self): ...

    @abstractmethod
    def get_exported_provider(self, token: InjectToken) -> Tuple[Optional[IProviderProxy], Optional[ProviderAnnotation]]: ...

    @abstractmethod
    def get_for_root_provider(self, token: InjectToken) -> Tuple[Optional[IProviderProxy], Optional[ProviderAnnotation]]: ...


@dataclass(frozen=True)
class ModuleAnnotation:
    imports: Modules
    providers: Providers
    for_root: bool = False


class IRootRunner(ABC):
    @abstractmethod
    def after_started(self, module_delegate: IModuleDelegate): ...


class IRootPlugin(ABC):
    @abstractmethod
    def __call__(self, root_module_delegate: IModuleDelegate): ...


Plugins = List[IRootPlugin]


class IProviderRunner(ABC):
    @abstractmethod
    def after_started(self): ...
