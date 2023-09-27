from dihub.decorators import provider, export, module
from fastapi import FastAPI


@export
@provider
class FastAPIProvider(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@module(providers=[FastAPIProvider])
class FastAPIModule: ...
