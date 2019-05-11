""" Fornece views para o app de lançamentos. """
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Conta, Journal, Lancamento
from .services import cria_lancamentos, atualiza_journals

def index(request):
    """ Exibe o painel inicial da aplicação. """
    return render(request, "lancamentos/painel.html")


class ExtratoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, mes, ano):
        cria_lancamentos(request.user, mes, ano)
        return Response()


class LancamentoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self):
        pass
    
    def post(self):
        pass
    
    def put(self):
        pass
    
    def delete(self):
        pass
