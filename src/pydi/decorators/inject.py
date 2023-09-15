from pydi.__internal.delegates import InjectedDelegate
from pydi.types import InjectToken


def inject(token: InjectToken) -> InjectedDelegate:
    return InjectedDelegate(token)
