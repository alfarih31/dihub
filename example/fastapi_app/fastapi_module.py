from fastapi import FastAPI

from dihub.decorators import provider, export, module


@export
@provider
class FastAPIProvider(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@module(providers=[FastAPIProvider])
class FastAPIModule: ...
