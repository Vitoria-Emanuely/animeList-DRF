from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.models import Genero
from core.serializers import GeneroSerializer


class GenerosListGeneric(ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer      

class GeneroDetailGeneric(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer  


