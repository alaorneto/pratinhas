""" Fornece views para o app de lançamentos. """
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Conta, Journal, Lancamento
from .serializers import JournalSerializer, LancamentoSerializer, ContaSerializer, CategoriaSerializer, UsuarioSerializer
from .services import criar_lancamentos, atualizar_journals, excluir_journal


def index(request):
    """ Exibe a página inicial da aplicação. """
    return render(request, "lancamentos/index.html")


def painel(request):
    """ Exibe o painel do usuário. """
    return render(request, "lancamentos/painel.html")


def extrato(request):
    """ Exibe o extrato do usuário. """
    return render(request, "lancamentos/extrato.html")


class UsuarioViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer


class ContaViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ContaSerializer

    def create(self, request):
        data = request.data
        data['proprietario'] = request.user.pk
        serializer = ContaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Conta.objects.proprietario(self.request.user).filter(conta_categoria=False)


class CategoriaViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        return Conta.objects.proprietario(self.request.user).filter(conta_categoria=True)


class ExtratoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, mes, ano):
        criar_lancamentos(request.user, mes, ano)
        return Response()


class LancamentoView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        serializer = LancamentoSerializer(get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        data['proprietario'] = request.user
        serializer = JournalSerializer(data)
        if serializer.is_valid():
            journal = serializer.save()
        return Response(journal)

    def retrieve(self, request, pk):
        lancamento = get_object_or_404(get_queryset(), pk)
        serializer = LancamentoSerializer(lancamento)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        lancamento = Lancamento.objects.proprietario(request.user).get_object_or_404(pk=pk)
        journal = lancamento.journal
        lancamento.delete()
        # verificar se foi selecionada a opção para excluir futuros
        excluir_journal(journal)
        raise NotImplemented()
    
    def get_queryset(self):
        return Lancamento.objects.proprietario(self.request.user)
    
    def get_serializer_class(self):
        """ 
        Define o serializer adequado dependendo da ação. 
        Em caso de criação de um novo lançamento, deve-se utilizar o serializer de Journals.
        Para as demais ações, é usado o serializer Lançamento.
        """
        if self.action == 'create':
            return JournalSerializer
        else:
            return LancamentoSerializer
