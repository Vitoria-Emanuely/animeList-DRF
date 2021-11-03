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
    titulo = models.CharField(max_length=255)
    genero = models.ManyToManyField(Genero, related_name="animes")
    estudio = models.ManyToManyField(Estudio, related_name="animes")
    epsT = models.IntegerField(verbose_name="Episodios Totais")

    def __str__(self):
        gen = ", ".join(str(i) for i in self.genero.all())
        return "%s (%s)" %(self.titulo, gen)


class Adiciona(models.Model):
    class Meta:
        verbose_name_plural = "Adiciona"
    class StatusAnime(models.TextChoices):
        ASSISTINDO = "Assistindo"
        COMPLETO = "Completo"
        QUERO_ASSISTIR = "Quero assistir"
        DESISTI = "Desisti"

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="adicoes")   
    status = models.CharField(max_length=255, choices=StatusAnime.choices, default=StatusAnime.ASSISTINDO)


class AdicionaAnimes(models.Model):
    adicao = models.ForeignKey(Adiciona, on_delete=models.CASCADE, related_name="animesAdd")
    anime = models.ForeignKey(Anime, on_delete=models.PROTECT, related_name="+")
    eps = models.IntegerField(verbose_name="Episodios")
    