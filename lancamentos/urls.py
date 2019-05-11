from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ContaViewSet, CategoriaViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('usuarios', UserViewSet)
router.register('contas', ContaViewSet, basename='conta')
router.register('categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', include(router.urls)),
]
