from dataclasses import dataclass

from dihub.types import InjectToken


@dataclass(frozen=True)
class InjectedDelegate:
    token: InjectToken
