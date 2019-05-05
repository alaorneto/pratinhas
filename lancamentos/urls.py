from django.urls import path
from lancamentos import views
from .views import ExtratoView, ContasList, ContaView

urlpatterns = [
    path('', views.index),
    path('contas/', ContasList.as_view()),
    path('conta/<int:conta_id>/', ContaView.as_view()),
    path('extrato/', ExtratoView.as_view())
]