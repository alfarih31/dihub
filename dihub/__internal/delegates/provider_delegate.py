from typing import Union, Tuple, List

from dihub.__internal.helpers import AnnotationOf, validate_dihub_provider, get_class_name, get_inject_token_str
from dihub.__internal.proxies import ProviderProxy
from dihub.constants import _PROVIDER_ANNOTATIONS
from dihub.exceptions import ProviderNotFound
from dihub.types import Providers, InjectToken, IProviderDelegate, ProviderAnnotation, Provide


class ProviderDelegate(IProviderDelegate):
    __providers: List[ProviderProxy]
    __iter_index = -1

    def __init__(self, providers: Providers):
        self.__providers = []
        for i in providers:
            validate_dihub_provider(i)

            self.__providers.append(ProviderProxy(i))

    def __str__(self):
        members_str = []
        for i in self.__providers:
            annotations = AnnotationOf(i.provide).get(_PROVIDER_ANNOTATIONS, ProviderAnnotation)
            members_str.append(
                "'%s': '%s'" % (annotations.token, get_class_name(i.provide)))
        return "{%s}" % (", ".join(members_str))

    def __add__(self, other: Union[IProviderDelegate, Providers]):
        if isinstance(other, ProviderDelegate):
            self.__providers += other.__providers
        else:
            for p in other:
                validate_dihub_provider(p)
                self.__providers.append(ProviderProxy(p))

        return self

    def __len__(self):
        return len(self.__providers)

    def append(self, item: Union[ProviderProxy, Provide]):
        if isinstance(item, ProviderProxy):
            self.__providers.append(item)
        else:
            validate_dihub_provider(item)
            self.__providers.append(ProviderProxy(item))
        return self

    def __iter__(self):
        self.__iter_index = -1
        return self

    def __next__(self) -> Tuple[ProviderProxy, ProviderAnnotation]:  # Python 2: def next(self)
        if self.__iter_index < len(self.__providers) - 1:
            self.__iter_index += 1
            p = self.__providers[self.__iter_index]
            annotations = AnnotationOf(p.provide).get(_PROVIDER_ANNOTATIONS, ProviderAnnotation)
            return p, annotations
        raise StopIteration

    def __is_token_match(self, this_token: str, that_token: InjectToken) -> bool:
        return get_inject_token_str(that_token) == this_token

    def __getitem__(self, token: InjectToken) -> Tuple[ProviderProxy, ProviderAnnotation]:
        for p in self.__providers:
            annotations = AnnotationOf(p.provide).get(_PROVIDER_ANNOTATIONS, ProviderAnnotation)

            if self.__is_token_match(annotations.token, token):
                return p, annotations

        raise ProviderNotFound(token)

    def __delitem__(self, token: InjectToken):
        for i, p in enumerate(self.__providers):
            annotations = AnnotationOf(p.provide).get(_PROVIDER_ANNOTATIONS, ProviderAnnotation)
            if self.__is_token_match(annotations.token, token):
                del self.__providers[i]
                return

    def on_boot(self):
        # Construct
        for i in self.__providers:
            i.on_boot()

    def on_post_boot(self):
        for i in self.__providers:
            i.on_post_boot()
