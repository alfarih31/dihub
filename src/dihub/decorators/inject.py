from dihub.__internal.delegates import InjectedDelegate
from dihub.types import InjectToken


def inject(token: InjectToken) -> InjectedDelegate:
    return InjectedDelegate(token)
