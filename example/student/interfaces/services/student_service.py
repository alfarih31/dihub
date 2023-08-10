from abc import abstractmethod, ABC
from typing import List

from student.models.student import Student


class IStudentService(ABC):
    @abstractmethod
    def create(self, student: Student) -> Student: ...

    @abstractmethod
    def get_all(self) -> List[Student]: ...
