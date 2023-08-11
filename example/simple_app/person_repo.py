from abc import ABC, abstractmethod
from typing import List, Set

from person import Person
from pydi.decorators import export, provider

PERSON_REPO = "PERSON_REPO"


class IPersonRepo(ABC):
    @abstractmethod
    def save(self, full_name: str) -> Person: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Person: ...

    @abstractmethod
    def find_all(self) -> List[Person]: ...


@export
@provider(PERSON_REPO)
class __PersonRepo(IPersonRepo):
    __in_memory: Set[Person]

    def __init__(self):
        self.__in_memory = set()

    def save(self, full_name: str) -> Person:
        p = Person(full_name=full_name)
        p.id = len(self.__in_memory)
        self.__in_memory.add(p)
        return p

    def find_all(self) -> List[Person]:
        return [x for x in self.__in_memory]

    def find_by_id(self, id: int) -> Person:
        for p in self.__in_memory:
            if p.id == id:
                return p
