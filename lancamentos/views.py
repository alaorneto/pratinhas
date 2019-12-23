""" Fornece views para o app de lançamentos. """
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Conta, Journal, Lancamento
from .serializers import JournalSerializer, LancamentoSerializer
from .serializers import ContaSerializer, CategoriaSerializer, UsuarioSerializer
from .services import atualizar_journals, excluir_journal


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

    def create(self, request):
        data = request.data
        data['proprietario'] = request.user.pk
        serializer = CategoriaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Conta.objects.proprietario(self.request.user).filter(conta_categoria=True)


class ExtratoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, mes, ano):
        atualizar_journals(request.user, mes, ano)
        return Response()


class LancamentoView(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        data = request.data
        data['proprietario'] = request.user.pk
        serializer = JournalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        lancamento = get_object_or_404(Lancamento.objects.proprietario(request.user), pk=pk)
        json = request.data
        serializer = LancamentoSerializer(lancamento, json)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        lancamento = get_object_or_404(Lancamento.objects.proprietario(request.user), pk=pk)
        data = lancamento.data
        journal = lancamento.journal
        lancamento.delete()

        if request.data.get("futuros"):
            Lancamento.objects.proprietario(request.user).filter(journal=journal.pk).filter(data__gt=data).delete()

        if not journal.tempo_indeterminado:
            if Lancamento.objects.proprietario(request.user).filter(journal=journal.pk).count() == 0:
                journal.delete()
                
        return Response(status=status.HTTP_200_OK)

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
