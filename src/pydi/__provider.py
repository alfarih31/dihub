from copy import deepcopy
from typing import Any, Optional

from pydi.constants import ProviderScope
from pydi.typing import IProvider, Provide, InjectToken


class Provider(IProvider):
    __token: InjectToken
    __provide: Provide
    __scope: ProviderScope

    def __init__(self, token: InjectToken, provide: Provide, scope: Optional[ProviderScope] = ProviderScope.GLOBAL):
        self.__token = token
        self.__provide = provide
        self.__scope = scope

    @property
    def token(self) -> InjectToken:
        return self.__token

    @property
    def provide(self):
        return self.__provide

    @property
    def scope(self) -> ProviderScope:
        return self.__scope

    def __copy__(self) -> IProvider:
        new_provide = deepcopy(self.provide)
        return Provider(self.token, new_provide)

    def __get__(self, *args, **kwargs):
        return self.provide

    def __str__(self):
        return "<token '%s'>%s" % (self.token, self.__provide)

    def __eq__(self, other: Any):
        if isinstance(other, Provider):
            return self.token == other.token
        elif isinstance(other, str):
            return self.token == other

        return False

    def __call__(self, *args, **kwargs):
        if isinstance(self.__provide, type):
            self.__provide = self.__provide()

    def __getattr__(self, item):
        return self.provide.__getattribute__(item)
