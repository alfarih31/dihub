from pydi import module
from .repositories import repositories
from .services import services


@module(providers=repositories + services)
class AModule: ...


@module(imports=[AModule], providers=[] + services)
class StudentModule: ...
