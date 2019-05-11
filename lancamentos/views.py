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
from .services import criar_lancamentos, atualizar_journals, excluir_journal

def index(request):
    """ Exibe o painel inicial da aplicação. """
    return render(request, "lancamentos/painel.html")


class ExtratoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, mes, ano):
        criar_lancamentos(request.user, mes, ano)
        return Response()


class LancamentoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        pass
    
    def post(self, request):
        pass
    
    def put(self, request, pk):
        pass
    
    def delete(self, request, pk):
        lancamento = Lancamento.objects.proprietario(request.user).get_object_or_404(pk=pk)
        journal = lancamento.journal
        lancamento.delete()
        excluir_journal(journal)
        pass
