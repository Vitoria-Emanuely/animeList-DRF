from rest_framework.viewsets import ModelViewSet
from core.models import Lista
from core.serializers import ListaSerializer, CriarEditarListaSerializer


class ListaViewSet(ModelViewSet):
    queryset = Lista.objects.all()
    # serializer_class = ListaSerializer

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ListaSerializer
        return CriarEditarListaSerializer
