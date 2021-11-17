from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer,
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from core.models import Genero, Estudio, Anime, Lista, ListaAnimes


class GeneroSerializer(ModelSerializer):
    class Meta:
        model = Genero
        fields = "__all__"


class GeneroNestedSerializer(ModelSerializer):
    class Meta:
        model = Genero
        fields = ("descricao",)


class EstudioSerializer(ModelSerializer):
    class Meta:
        model = Estudio
        fields = "__all__"


class EstudioNestedSerializer(ModelSerializer):
    class Meta:
        model = Estudio
        fields = ("nome",)


class AnimeSerializer(ModelSerializer):
    class Meta:
        model = Anime
        fields = "__all__"

    def to_representation(self, instance):
        self.fields["genero"] = GeneroNestedSerializer(many=True)
        self.fields["estudio"] = EstudioNestedSerializer(many=True)
        return super().to_representation(instance)


# class AnimeDetailSerializer(ModelSerializer):
# genero = SlugRelatedField(
#     many=True, read_only=True, slug_field="nome"
# )
# genero = SlugRelatedField(many=True, read_only=True,
# slug_field="descricao")
# estudio = EstudioNestedSerializer(many=True)
# genero = GeneroNestedSerializer(many=True)

# class Meta:
#     model = Anime
#     fields = "__all__"
# depth = 1

# def get_genero(self, instance):
#     descricoes_generos = []
#     genero = instance.genero.get_queryset()
#     for i in genero:
#         descricoes_generos.append(i.descricao)
#     return descricoes_generos


class ListaAnimesSerializer(ModelSerializer):
    eps_faltam = SerializerMethodField()

    class Meta:
        model = ListaAnimes
        fields = ("anime", "status", "eps", "eps_faltam")
        depth = 2

    def get_eps_faltam(self, instance):
        return instance.anime.epsT - instance.eps


class ListaSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email")
    lista_animes = ListaAnimesSerializer(many=True)

    class Meta:
        model = Lista
        fields = ("id", "usuario", "lista_animes")


class CriarEditarListaAnimesSerializer(ModelSerializer):
    class Meta:
        model = ListaAnimes
        fields = ("anime", "eps", "status")


class CriarEditarListaSerializer(ModelSerializer):
    lista_animes = CriarEditarListaAnimesSerializer(many=True)

    class Meta:
        model = Lista
        fields = ("usuario", "lista_animes")

    def create(self, validated_data):

        lista_animes = validated_data.pop("lista_animes")
        breakpoint()
        try:
            lista = Lista.objects.get(usuario=validated_data.get("usuario"))
        except Exception:
            lista = Lista.objects.create(**validated_data)

        for i in lista_animes:
            ListaAnimes.objects.create(lista=lista, **i)
        lista.save()
        return lista

    def update(self, instance, validated_data):
        lista_animes = validated_data.pop("lista_animes")
        if lista_animes:
            instance.lista_animes.all().delete()
            for i in lista_animes:
                ListaAnimes.objects.create(lista=instance, **i)
            instance.save()
        return instance


class UsuarioSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "lista")
        read_only_fields = ["lista"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        instance = super().create(validated_data)
        # Lista.objects.create(usuario=instance)
        # instance.lista = lista
        return instance

    def update(self, instance, validated_data):
        password = validated_data.get("password", False)
        if password:
            validated_data["password"] = make_password(password)
        return super().update(instance, validated_data)
