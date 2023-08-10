from dataclasses import dataclass

from pydi.constants import ProviderScope


@dataclass(frozen=True)
class ProviderAnnotation:
    token: str
    scope: ProviderScope
    exported: bool = False
