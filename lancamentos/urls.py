from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .viewsets import UsuarioViewSet, ContaViewSet, CategoriaViewSet, JournalViewSet, LancamentoViewSet


router = routers.DefaultRouter()
router.register('usuarios', UsuarioViewSet)
router.register('contas', ContaViewSet, basename='conta')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('journals', JournalViewSet, basename='journal')
router.register('lancamentos', LancamentoViewSet, basename='lancamento')

urlpatterns = router.urls