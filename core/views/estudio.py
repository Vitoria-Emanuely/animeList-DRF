from rest_framework.viewsets import ModelViewSet
from core.models import Estudio
from core.serializers import EstudioSerializer


class EstudioViewSet(ModelViewSet):
    queryset = Estudio.objects.all()
    serializer_class = EstudioSerializer
