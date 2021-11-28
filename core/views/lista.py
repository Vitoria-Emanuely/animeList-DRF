from rest_framework.viewsets import ModelViewSet
from core.models import Lista
from core.serializers import ListaSerializer, CriarEditarListaSerializer


class ListaViewSet(ModelViewSet):
    queryset = Lista.objects.all()

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ListaSerializer
        return CriarEditarListaSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.groups.filter(name="Administradores"):
            return Lista.objects.all()
        return Lista.objects.filter(usuario=usuario)
