from abc import ABC, abstractmethod
from typing import List, Annotated

from dihub.decorators import inject, provider
from person import Person
from person_repo import IPersonRepo, PERSON_REPO

PERSON_SERVICE = "PERSON_SERVICE"


class IPersonService(ABC):
    @abstractmethod
    def register(self, full_name: str): ...

    @abstractmethod
    def get(self, id: int) -> Person: ...

    @abstractmethod
    def get_all(self) -> List[Person]: ...


@provider(token=PERSON_SERVICE)
class __PersonService(IPersonService):
    person_repo: Annotated[IPersonRepo, inject(PERSON_REPO)]

    def register(self, full_name: str):
        self.person_repo.save(full_name)

    def get(self, id: int) -> Person:
        return self.person_repo.find_by_id(id)

    def get_all(self) -> List[Person]:
        return self.person_repo.find_all()
