from typing import Set, List

from pydi import provider, export, ProviderScope
from student.interfaces.repositories.student_repository import IStudentRepository
from student.models.student import Student
from student.student_tokens import STUDENT_REPOSITORY


@export
@provider(STUDENT_REPOSITORY, scope=ProviderScope.LOCAL)
class StudentRepository(IStudentRepository):
    __in_memory: Set[Student]

    def __init__(self):
        self.__in_memory = set()

    def save(self, student: Student) -> Student:
        student.id = len(self.__in_memory)
        self.__in_memory.add(student)
        return student

    def find_all(self) -> List[Student]:
        return [x for x in self.__in_memory]
