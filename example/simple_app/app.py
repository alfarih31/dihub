from person_repo import __PersonRepo
from person_service import __PersonService, PERSON_SERVICE, IPersonService
from pydi.decorators import module, root


@root
@module(providers=[__PersonRepo, __PersonService])
class App: ...


if __name__ == "__main__":
    root_app = App()
    person_service: IPersonService = root_app[(App, PERSON_SERVICE)]
    person_service.register("John Doe")
    all_person = person_service.get_all()
    print("All person:", all_person)
    person = person_service.get(person_service.get_all()[0].id)
    print("John Doe:", person)
