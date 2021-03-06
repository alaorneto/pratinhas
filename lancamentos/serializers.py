""" Serializers do módulo de lançamentos. """
import numbers
from django.contrib.auth.models import User
from .models import Conta, Journal, Lancamento
from rest_framework import serializers


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')


class ContaSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if 'data_inicial' in data:
            if not data['data_inicial']:
                raise serializers.ValidationError("É necessário indicar a data inicial da conta.")
        else:
            raise serializers.ValidationError("É necessário indicar a data inicial da conta.")
        if 'saldo_inicial' in data:
            if not isinstance(data['saldo_inicial'], numbers.Number):
                raise serializers.ValidationError("É necessário indicar o saldo inicial da conta.")
        else:
            raise serializers.ValidationError("É necessário indicar o saldo inicial da conta.")
        return data

    def create(self, validated_data):
        conta = Conta(**validated_data)
        conta.conta_categoria = False
        conta.save()
        return conta

    class Meta:
        model = Conta
        fields = ('pk', 'data_inicial', 'saldo_inicial', 'nome', 'proprietario')


class CategoriaSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if 'data_inicial' in data:
            raise serializers.ValidationError("Uma categoria não deve ter data inicial.")
        if 'saldo_inicial' in data:
            raise serializers.ValidationError("Uma categoria não deve ter saldo inicial")
        return data
    
    def create(self, validated_data):
        categoria = Conta(**validated_data)
        categoria.conta_categoria = True
        categoria.save()
        return categoria

    class Meta:
        model = Conta
        fields = ('nome', 'proprietario')


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('pk', 'tipo', 'data', 'conta_debito', 'conta_credito',
                  'valor', 'periodicidade', 'tempo_indeterminado', 'parcela_inicial',
                  'qtde_parcelas', 'ultima_atualizacao', 'proprietario')


class LancamentoSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.data = validated_data.get('data', instance.data)
        instance.conta_debito = validated_data.get('conta_debito', instance.conta_debito)
        instance.conta_credito = validated_data.get('conta_credito', instance.conta_credito)
        instance.valor = validated_data.get('valor', instance.valor)
        instance.save()
        return instance
    
    def get_data(self):
        return self.data

    class Meta:
        model = Lancamento
        fields = ('journal', 'data', 'conta_debito', 'conta_credito', 'valor', 'num_parcela', 'proprietario')
