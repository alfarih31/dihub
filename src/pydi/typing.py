from abc import abstractmethod, ABC
from typing import TypeAlias, TypeVar, Callable, List, Optional, Union, Tuple, Self, TypeGuard

from pydi.constants import ProviderScope

_Instance = TypeVar('_Instance', bound=type)
Value = TypeVar("Value", covariant=True)
Method: TypeAlias = Callable[[_Instance], Value]

InjectToken: TypeAlias = str

_as_class: TypeAlias = type
_as_primitive: TypeAlias = Union[str, int, bool, float]

# Provide: TypeAlias = Union[_as_primitive, _as_class]
Provide = TypeVar("Provide", bound=Union[Callable[..., _as_primitive], type])


class IProvider(ABC):
    @property
    @abstractmethod
    def token(self) -> InjectToken: ...

    @property
    @abstractmethod
    def provide(self) -> Provide: ...

    @property
    @abstractmethod
    def scope(self) -> ProviderScope: ...

    @abstractmethod
    def __copy__(self) -> Self: ...


Providers: TypeAlias = List[Provide]

Modules: TypeAlias = List[type]


class IModuleDelegate(ABC):
    @abstractmethod
    def __getitem__(self, attr: Tuple[Union[type, Self], InjectToken]) -> Optional[Provide]: ...

    def __call__(self, *args, **kwargs) -> Self: ...


def is_not_none(a: Value) -> TypeGuard[Value]:
    return a is not None
