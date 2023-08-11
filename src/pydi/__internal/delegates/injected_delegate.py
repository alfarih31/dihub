from dataclasses import dataclass

from pydi.typing import InjectToken


@dataclass(frozen=True)
class InjectedDelegate:
    token: InjectToken
