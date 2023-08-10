from abc import ABCMeta, abstractmethod
from typing import List

from student.models.student import Student


class IStudentRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, student: Student) -> Student: ...

    @abstractmethod
    def find_all(self) -> List[Student]: ...
