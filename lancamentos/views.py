""" Fornece views para o app de lançamentos. """
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Conta, Categoria, Journal, Lancamento
from .serializers import UserSerializer, ContaSerializer, CategoriaSerializer
from rest_framework import permissions, viewsets

def index(request):
    """ Exibe o painel inicial da aplicação. """
    return render(request, "lancamentos/painel.html")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ContaViewSet(viewsets.ModelViewSet):
    serializer_class = ContaSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        usuario = self.request.user
        return Conta.objects.proprietario(usuario)


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        usuario = self.request.user
        return Categoria.objects.proprietario(usuario)