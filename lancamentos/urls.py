from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .views import ExtratoView, LancamentoView, UsuarioViewSet, ContaViewSet, CategoriaViewSet
from .views import index, extrato, painel

router = routers.DefaultRouter()
router.register('usuarios', UsuarioViewSet)
router.register('contas', ContaViewSet, basename='conta')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('lancamentos', LancamentoView, basename='lancamento')

urlpatterns = [
    path('extrato/', extrato),
    path('painel/', painel),
    path('extrato/<int:mes>/<int:ano>/', ExtratoView.as_view()),
    url('api/core/', include(router.urls)),
    path('', index),
]
