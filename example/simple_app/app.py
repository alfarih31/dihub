from person_repo import __PersonRepo
from person_service import __PersonService, PERSON_SERVICE, IPersonService
from dihub.decorators import module, root
from dihub.types import IRootRunner, IModuleDelegate


@root
@module(providers=[__PersonRepo, __PersonService])
class App(IRootRunner):
    var: int

    def after_started(self, root_app: IModuleDelegate):
        person_service = root_app.providers[PERSON_SERVICE][0].cast(IPersonService)
        person_service.register("John Doe")
        all_person = person_service.get_all()
        print("All person:", all_person)
        person = person_service.get(person_service.get_all()[0].id)
        print("John Doe:", person)


if __name__ == "__main__":
    a = App()
    print(a, App)
