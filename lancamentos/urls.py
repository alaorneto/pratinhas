from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .viewsets import UsuarioViewSet, ContaViewSet, CategoriaViewSet
from .views import ExtratoView, LancamentoView
import lancamentos.views as views

router = routers.DefaultRouter()
router.register('usuarios', UsuarioViewSet)
router.register('contas', ContaViewSet, basename='conta')
router.register('categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    url('api/core/', include(router.urls)),
    path('extrato/<int:mes>/<int:ano>/', ExtratoView.as_view()),
    path('lancamento/<int:pk>/', LancamentoView.as_view()),
    path('', views.index),
]
