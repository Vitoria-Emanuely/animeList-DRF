from rest_framework.viewsets import ModelViewSet
from core.models import Genero
from core.serializers import GeneroSerializer


class GeneroViewSet(ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
