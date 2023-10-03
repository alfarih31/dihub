from abc import abstractmethod, ABC
from dataclasses import dataclass
from types import FunctionType, LambdaType
from typing import TypeAlias, TypeVar, Callable, List, Union, Self, Tuple, Optional, Any, Type, Protocol

from .constants import ProviderScope

Value = TypeVar("Value", covariant=True)
Config = TypeVar("Config", contravariant=True)


class Configurable(Protocol[Config, Value]):
    @classmethod
    @abstractmethod
    def configure(cls, Config: Config) -> Value: ...

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Value: ...


Instance = TypeVar('Instance', type, Configurable, covariant=True)
Method: TypeAlias = Callable[[Instance], Value]

NOTABLE = Union[type, FunctionType, LambdaType]

InjectToken = Union[str, type]

_as_class: TypeAlias = type
_as_primitive: TypeAlias = Union[str, int, bool, float]

Provide = TypeVar("Provide", covariant=True)

Modules: TypeAlias = List[Instance]


def is_notable(obj) -> bool:
    return isinstance(obj, FunctionType) or isinstance(obj, LambdaType) or isinstance(obj, type)


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
    @property
    @abstractmethod
    def is_root(self) -> bool: ...

    @abstractmethod
    def __getitem__(self, module: Instance) -> Self: ...

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Self: ...

    @abstractmethod
    def deep_eq(self, other: Any) -> bool: ...

    @property
    @abstractmethod
    def providers(self) -> IProviderDelegate: ...

    @property
    @abstractmethod
    def imports(self) -> List[Self]: ...

    @property
    @abstractmethod
    def base_class(self) -> type: ...

    @property
    @abstractmethod
    def root_delegate(self) -> Self: ...

    @property
    @abstractmethod
    def parent_delegate(self) -> Self: ...

    @abstractmethod
    def on_boot(self): ...

    @abstractmethod
    def on_post_boot(self): ...

    @abstractmethod
    def get_exported_provider(self, token: str) -> Tuple[Optional[IProviderProxy], Optional[ProviderAnnotation]]: ...

    @abstractmethod
    def get_for_root_provider(self, token: str) -> Tuple[Optional[IProviderProxy], Optional[ProviderAnnotation]]: ...


@dataclass(frozen=True)
class ModuleAnnotation:
    imports: Modules
    providers: Providers
    for_root: bool = False


class IRootRunner(ABC):
    def __await__(self): ...

    @abstractmethod
    def after_started(self, root_module_delegate: IModuleDelegate): ...


class IConfigurableModule(Protocol[Value]):
    __config: Value

    @property
    def Config(self) -> Value:
        return self.__config

    def configure(self, config: Value):
        self.__config = config


class IRootPlugin(ABC):
    @abstractmethod
    def __call__(self, root_module_delegate: IModuleDelegate): ...


Plugins = List[IRootPlugin]


class IProviderRunner(ABC):
    @abstractmethod
    def after_started(self): ...


class IInjectedDelegate(ABC):
    @property
    @abstractmethod
    def token(self) -> str: ...
