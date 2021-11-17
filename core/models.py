from django.db import models
from django.contrib.auth.models import User


class Genero(models.Model):
    class Meta:
        verbose_name_plural = "Generos"

    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao


class Estudio(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Anime(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    genero = models.ManyToManyField(Genero, related_name="animes")
    estudio = models.ManyToManyField(Estudio, related_name="animes")
    epsT = models.IntegerField(verbose_name="Episodios Totais")

    def __str__(self):
        gen = ", ".join(str(i) for i in self.genero.all())
        return "%s (%s)" % (self.titulo, gen)


class Lista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT, related_name="lista")

    # @property
    # def epsA_total(self):
    #     queryset = self.animesAdd.all().aggregate(epsA_total=models.Sum("eps"))
    #     return queryset["epsA_total"]


# class Usuario(User):
#     @classmethod
#     def create(cls, username, password):
#         usuario = cls(username=username, password=password)
#         Lista.objects.create(usuario=usuario)
#         return usuario


class ListaAnimes(models.Model):
    lista = models.ForeignKey(
        Lista, on_delete=models.CASCADE, related_name="lista_animes"
    )

    class StatusAnime(models.TextChoices):
        ASSISTINDO = "Assistindo"
        COMPLETO = "Completo"
        QUERO_ASSISTIR = "Quero assistir"
        DESISTI = "Desisti"

    status = models.CharField(
        max_length=255, choices=StatusAnime.choices, default=StatusAnime.ASSISTINDO
    )
    anime = models.ForeignKey(Anime, on_delete=models.PROTECT, related_name="+")
    eps = models.IntegerField(verbose_name="Episodios")
