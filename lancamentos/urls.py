from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .views import ExtratoView, LancamentoView, UsuarioViewSet, ContaViewSet, CategoriaViewSet

router = routers.DefaultRouter()
router.register('usuarios', UsuarioViewSet)
router.register('contas', ContaViewSet, basename='conta')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('lancamentos', LancamentoView, basename='lancamento')

urlpatterns = [
    path('extrato/<int:mes>/<int:ano>/', ExtratoView.as_view()),
    url('', include(router.urls)),
]
