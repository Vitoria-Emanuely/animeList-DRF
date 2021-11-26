from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Genero(models.Model):
    descricao = models.CharField("Descrição", max_length=100)

    def __str__(self):
        return self.descricao


class Estudio(models.Model):
    nome = models.CharField("Nome", max_length=100)

    def __str__(self):
        return self.nome


class Anime(models.Model):
    titulo = models.CharField("Título", max_length=255, unique=True)
    genero = models.ManyToManyField(
        Genero, verbose_name="Gênero", related_name="animes"
    )
    estudio = models.ManyToManyField(
        Estudio, verbose_name="Estúdio", related_name="animes"
    )
    epsT = models.PositiveIntegerField(verbose_name="Episódios Totais")

    def __str__(self):
        gen = ", ".join(str(i) for i in self.genero.all())
        return "%s (%s)" % (self.titulo, gen)


class Lista(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.PROTECT, verbose_name="Usuário", related_name="lista"
    )

    @property
    def epsA_total(self):
        queryset = self.lista_animes.all().aggregate(epsA_total=models.Sum("eps"))
        return queryset["epsA_total"]


# class Usuario(User):
#     @classmethod
#     def create(cls, username, password):
#         usuario = cls(username=username, password=password)
#         Lista.objects.create(usuario=usuario)
#         return usuario


class ListaAnimes(models.Model):
    class Meta:
        verbose_name_plural = "Lista Animes"

    lista = models.ForeignKey(
        Lista, on_delete=models.CASCADE, related_name="lista_animes"
    )

    class StatusAnime(models.TextChoices):
        ASSISTINDO = "Assistindo"
        COMPLETO = "Completo"
        QUERO_ASSISTIR = "Quero assistir"
        DESISTI = "Desisti"

    status = models.CharField(
        "Status",
        max_length=255,
        choices=StatusAnime.choices,
        default=StatusAnime.ASSISTINDO,
    )
    anime = models.ForeignKey(
        Anime,
        on_delete=models.PROTECT,
        related_name="+",
    )
    eps = models.PositiveIntegerField("Episódios")

    def clean(self):
        if self.eps > self.anime.epsT:
            raise ValidationError("O número máximo de eps é %d" % self.anime.epsT)
        if self.eps == self.anime.epsT:
            self.status = "Completo"
        if self.eps < self.anime.epsT and self.status == "Completo":
            raise ValidationError("Status inválido")
