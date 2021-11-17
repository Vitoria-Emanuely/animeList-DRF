from .generoClass import GeneroView
from .generoApiView import GeneroDetail, GenerosList
from .generoGeneric import GeneroDetailGeneric, GenerosListGeneric
from .genero import GeneroViewSet
from .estudio import EstudioViewSet
from .lista import ListaViewSet
from .anime import AnimeViewSet

__all__ = [
    "GeneroView",
    "GeneroDetail",
    "GenerosList",
    "GeneroDetailGeneric",
    "GenerosListGeneric",
    "GeneroViewSet",
    "EstudioViewSet",
    "AnimeViewSet",
    "ListaViewSet",
]
