from django.contrib.auth.models import User
from .models import Conta, Journal, Lancamento
from rest_framework import serializers


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ContaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conta
        fields = ('data_inicial', 'saldo_inicial', 'nome', 'proprietario')


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conta
        fields = ('nome', 'proprietario')


class JournalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Journal
        fields = ('data', 'conta_debito', 'conta_credito', 'valor', 'proprietario')


class LancamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lancamento
        fields = ('data', 'conta_debito', 'conta_credito', 'valor', 'proprietario')
