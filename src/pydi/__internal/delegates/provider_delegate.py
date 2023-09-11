from typing import Union, Tuple, List

from pydi.__internal.proxies import ProviderProxy
from pydi.constants import _PROVIDER_ANNOTATIONS
from pydi.exceptions import NotAPyDIProvider, ProviderNotFound
from pydi.types import Providers, InjectToken, IProviderDelegate, ProviderAnnotation


class ProviderDelegate(IProviderDelegate):
    __providers: List[ProviderProxy]
    __iter_index = -1

    def __init__(self, providers: Providers):
        self.__providers = []
        for i in providers:
            if i.__annotations__.get(_PROVIDER_ANNOTATIONS) is None:
                raise NotAPyDIProvider(i.__name__)

            self.__providers.append(ProviderProxy(i))

    def __str__(self):
        members_str = []
        for i in self.__providers:
            members_str.append(str(i))
        return "[%s]" % (", ".join(members_str))

    def __add__(self, other: Union[IProviderDelegate, Providers]):
        if isinstance(other, ProviderDelegate):
            self.__providers += other.__providers
        else:
            self.__providers += other

    def append(self, item: ProviderProxy):
        self.__providers.append(item)
        return self

    def __iter__(self):
        self.__iter_index = -1
        return self

    def __next__(self) -> Tuple[ProviderProxy, ProviderAnnotation]:  # Python 2: def next(self)
        if self.__iter_index < len(self.__providers) - 1:
            self.__iter_index += 1
            p = self.__providers[self.__iter_index]
            annotations: ProviderAnnotation = p.provide.__annotations__.get(_PROVIDER_ANNOTATIONS)
            return p, annotations
        raise StopIteration

    def __getitem__(self, token: InjectToken) -> Tuple[ProviderProxy, ProviderAnnotation]:
        for p in self.__providers:
            annotations: ProviderAnnotation = p.provide.__annotations__.get(_PROVIDER_ANNOTATIONS)
            if annotations.token == token:
                return p, annotations

        raise ProviderNotFound(token)

    def __delitem__(self, token: InjectToken):
        for i, p in enumerate(self.__providers):
            annotations: ProviderAnnotation = p.provide.__annotations__.get(_PROVIDER_ANNOTATIONS)
            if annotations.token == token:
                del self.__providers[i]
                return

    def on_boot(self):
        # Construct
        for i in self.__providers:
            i.on_boot()

    def on_post_boot(self):
        for i in self.__providers:
            i.on_post_boot()
