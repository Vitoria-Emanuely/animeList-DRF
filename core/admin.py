from django.contrib import admin

from core.models import Genero, Estudio, Anime, Lista, ListaAnimes

admin.site.register(Genero)
admin.site.register(Estudio)
admin.site.register(Anime)


class ItensInInline(admin.TabularInline):
    model = ListaAnimes
    # max_num = 1


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    inlines = (ItensInInline,)
