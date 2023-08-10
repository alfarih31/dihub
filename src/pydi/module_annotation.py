from dataclasses import dataclass

from pydi.typing import Modules, Providers


@dataclass(frozen=True)
class ModuleAnnotation:
    imports: Modules
    providers: Providers
