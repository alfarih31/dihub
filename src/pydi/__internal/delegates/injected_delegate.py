from dataclasses import dataclass

from pydi.types import InjectToken


@dataclass(frozen=True)
class InjectedDelegate:
    token: InjectToken
