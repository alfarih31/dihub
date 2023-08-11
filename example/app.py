from pydi.decorators import module, root
from pydi.typing import IModuleDelegate
from student import StudentModule, AModule
from student.interfaces.repositories.student_repository import IStudentRepository
from student.interfaces.services.student_service import IStudentService
from student.models.student import Student
from student.student_tokens import STUDENT_SERVICE


@root
@module(imports=[StudentModule])
class App: ...


def bootstrap(root_container: IModuleDelegate):
    print(root_container)
    student_service_from_original: IStudentService = root_container[(StudentModule, STUDENT_SERVICE)]
    student_service_from_a: IStudentService = root_container[(AModule, STUDENT_SERVICE)]
    print("FROM A", student_service_from_a)  # student.services.student_service
    print("FROM ORI", student_service_from_original)  # student.services.student_service
    rp_a: IStudentRepository = getattr(student_service_from_a, "student_repo")
    rp_ori: IStudentRepository = getattr(student_service_from_original, "student_repo")
    rp_ori.save(Student(full_name="John Doe Original"))
    rp_a.save(Student(full_name="John Doe A"))

    print(rp_a.find_all(), student_service_from_a.get_all())
    print(rp_ori.find_all(), student_service_from_original.get_all())


if __name__ == "__main__":
    root_module = App()
    bootstrap(root_module)
