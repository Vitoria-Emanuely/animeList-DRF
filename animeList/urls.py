"""animeList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


router = routers.DefaultRouter()
router.register(r"generos", views.GeneroViewSet)
router.register(r"estudios", views.EstudioViewSet)
router.register(r"animes", views.AnimeViewSet)
router.register(r"lista", views.ListaViewSet)
# router.register(r"usuarios", views.UsuarioViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Autenticação (Simple JWT)
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # OpenAPI 3
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Outros endpoints
    path("generos-class/", views.GeneroView.as_view()),
    path("generos-class/<int:id>/", views.GeneroView.as_view()),
    path("generos-apiview/", views.GenerosList.as_view()),
    path("generos-apiview/<int:id>/", views.GeneroDetail.as_view()),
    path("generos-generic/", views.GenerosListGeneric.as_view()),
    path("generos-generic/<int:id>/", views.GeneroDetailGeneric.as_view()),
    path("api/", include(router.urls)),
]
