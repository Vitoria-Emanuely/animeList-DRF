from rest_framework.viewsets import ModelViewSet
from core.models import Anime
from core.serializers import AnimeSerializer


class AnimeViewSet(ModelViewSet):
    queryset = Anime.objects.all()
    # serializer_class = AnimeSerializer

    def get_serializer_class(self):
        # if self.action == "list" or self.action == "retrieve":
        #     return AnimeDetailSerializer
        return AnimeSerializer
