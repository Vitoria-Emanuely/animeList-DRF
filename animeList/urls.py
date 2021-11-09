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

router = routers.DefaultRouter()
router.register(r'generos-viewset', views.GeneroViewSet)
router.register(r'estudios-viewset', views.EstudioViewSet)
# router.register(r'animes-viewset', views.AnimeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generos/', views.GeneroView.as_view()),
    path('generos/<int:id>/', views.GeneroView.as_view()),
    path('generos-apiview/', views.GenerosList.as_view()),
    path('generos-apiview/<int:id>/', views.GeneroDetail.as_view()),
    path('generos-generic/', views.GenerosListGeneric.as_view()),
    path('generos-generic/<int:id>/', views.GeneroDetailGeneric.as_view()),
    path('', include(router.urls))
]
