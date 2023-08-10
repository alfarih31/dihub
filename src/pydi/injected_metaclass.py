from typing import Generic

from pydi.typing import InjectToken, Value


class InjectedMetaclass(Generic[Value]):
    __token: InjectToken

    def __init__(self, token: InjectToken) -> None:
        self.__token = token

    @property
    def token(self):
        return self.__token
