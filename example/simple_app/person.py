from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class Person:
    full_name: str
    id: int = field(init=False)
