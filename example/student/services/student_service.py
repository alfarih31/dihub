from typing import List

from pydi import inject, provider, export
from student.interfaces.repositories.student_repository import IStudentRepository
from student.interfaces.services.student_service import IStudentService
from student.models.student import Student
from student.student_tokens import STUDENT_REPOSITORY, STUDENT_SERVICE


@export
@provider(STUDENT_SERVICE)
class StudentService(IStudentService):
    student_repo: IStudentRepository = inject(STUDENT_REPOSITORY)
    student_repo2: IStudentRepository = inject(STUDENT_REPOSITORY)

    def create(self, s: Student) -> Student:
        student = self.student_repo.save(Student(full_name=s.full_name))
        return student

    def get_all(self) -> List[Student]:
        return self.student_repo.find_all()
