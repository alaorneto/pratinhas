from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Conta, Journal, Lancamento
from .serializers import UsuarioSerializer, ContaSerializer, CategoriaSerializer, JournalSerializer, LancamentoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer


class ContaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContaSerializer

    def get_queryset(self):
        usuario = self.request.user
        return Conta.objects.proprietario(usuario).filter(conta_categoria=False)


class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        usuario = self.request.user
        return Conta.objects.proprietario(usuario).filter(conta_categoria=True)
