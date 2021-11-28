from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import (
    ModelSerializer,
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from core.models import Genero, Estudio, Anime, Lista, ListaAnimes
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers


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
        fields = ("usuario", "lista_animes", "epsA_total")


class CriarEditarListaAnimesSerializer(ModelSerializer):
    def validate(self, attr):
        anime = attr.get("anime")
        if attr["eps"] > anime.epsT:
            raise ValidationError("O número máximo de eps é %d" % anime.epsT)
        if attr["eps"] == anime.epsT:
            attr["status"] = "Completo"
        if attr["eps"] < anime.epsT and attr["status"] == "Completo":
            raise ValidationError("Status inválido")
        return attr

    class Meta:
        model = ListaAnimes
        fields = ("id", "anime", "eps", "status")


class CriarEditarListaSerializer(ModelSerializer):
    lista_animes = CriarEditarListaAnimesSerializer(many=True)
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lista
        fields = ("usuario", "lista_animes")

    def create(self, validated_data):
        lista_animes = validated_data.pop("lista_animes")
        try:
            lista = Lista.objects.get(usuario=validated_data.get("usuario"))
        except Exception:
            lista = Lista.objects.create(**validated_data)
        for i in lista_animes:
            ListaAnimes.objects.create(lista=lista, **i)
        lista.save()
        return lista

    @transaction.atomic
    def update(self, instance, validated_data):
        lista_animes = validated_data.pop("lista_animes")
        animes = ListaAnimes.objects.filter(lista=instance)
        for i in lista_animes:
            achou = False
            for j in animes:
                if i.get("anime") == j.anime:
                    achou = True
                    if i.get("eps"):
                        j.eps = i.get("eps")
                    if i.get("status"):
                        j.status = i.get("status")
                    j.save()
                    break
            if achou is False:
                ListaAnimes.objects.create(lista=instance, **i)
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
