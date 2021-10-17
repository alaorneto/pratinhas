from django.urls import path, include
from rest_framework import routers
from .views import ExtratoView, LancamentoView, ContaViewSet, CategoriaViewSet
from .views import painel

router = routers.DefaultRouter()
router.register('contas', ContaViewSet, basename='conta')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('lancamentos', LancamentoView, basename='lancamento')

urlpatterns = [
    path('painel/', painel),
    path('extrato/<int:mes>/<int:ano>/', ExtratoView.as_view()),
    path('extrato/<int:mes>/<int:ano>/<int:pk>/', ExtratoView.as_view()),
    path('', include(router.urls)),
]
