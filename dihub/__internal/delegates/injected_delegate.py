from dihub.__internal.helpers import get_inject_token_str
from dihub.types import InjectToken, IInjectedDelegate


class InjectedDelegate(IInjectedDelegate):
    __token: InjectToken

    def __init__(self, token: InjectToken):
        self.__token = get_inject_token_str(token)

    @property
    def token(self) -> str:
        return self.__token

    def __repr__(self):
        return "InjectedDelegate(token=%s)" % self.token
