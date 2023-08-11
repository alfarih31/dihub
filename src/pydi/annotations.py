from dataclasses import dataclass

from pydi.constants import ProviderScope
from pydi.typing import Modules, Providers


@dataclass(frozen=True)
class ModuleAnnotation:
    imports: Modules
    providers: Providers


@dataclass(frozen=True)
class ProviderAnnotation:
    token: str
    scope: ProviderScope
    exported: bool = False
