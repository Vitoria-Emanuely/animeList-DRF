from django.contrib import admin

from core.models import Genero, Estudio, Anime, Adiciona, AdicionaAnimes

admin.site.register(Genero)
admin.site.register(Estudio)
admin.site.register(Anime)


class ItensInInline(admin.TabularInline):
    model = AdicionaAnimes
    max_num = 1

@admin.register(Adiciona)
class AdicionaAdmin(admin.ModelAdmin):
    inlines = (ItensInInline,) 
    