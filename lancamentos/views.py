""" Fornece views para o app de lançamentos. """
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Conta, Categoria, Journal, Lancamento

def index(request):
    """ Exibe o painel inicial da aplicação. """
    return render(request, "lancamentos/painel.html")


DECORATORS = [login_required]


@method_decorator(DECORATORS, name='dispatch')
class ExtratoView(View):
    """ Fornece uma API para dados de extrato. """

    def get(self, request):
        pass


@method_decorator(DECORATORS, name='dispatch')
class ContasList(View):
    """ Fornece uma API para dados de conta. """

    def get(self, request):
        contas = Conta.objects.proprietario(request.user)
        response = {"data": list(contas.values())}
        return JsonResponse(response)


@method_decorator(DECORATORS, name='dispatch')
class ContaView(View):
    """ Fornece uma API para dados de conta. """

    def get(self, request, *args, **kwargs):
        conta = get_object_or_404(Conta.objects.proprietario(request.user).values(), pk=self.kwargs['conta_id'])
        response = {"data": conta}
        return JsonResponse(response)


@method_decorator(DECORATORS, name='dispatch')
class CategoriaView(View):
    """ Fornece uma API para dados de categoria. """

    def get(self, request):
        categorias = Categoria.objects.proprietario(request.user)
        response = {"data": list(categorias.values())}
        return JsonResponse(response)


@method_decorator(DECORATORS, name='dispatch')
class LancamentoView(View):
    """ Fornece uma API para dados de lançamento. """

    def get(self, request):
        pass