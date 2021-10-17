""" Serializers do módulo de lançamentos. """
import numbers
from .models import Conta, Journal, Lancamento
from rest_framework import serializers


class ContaSerializer(serializers.ModelSerializer):
    saldo_atual = serializers.ReadOnlyField()
    
    def validate(self, attrs):
        if 'data_inicial' in attrs:
            if not attrs['data_inicial']:
                raise serializers.ValidationError("É necessário indicar a data inicial da conta.")
        else:
            raise serializers.ValidationError("É necessário indicar a data inicial da conta.")
        if 'saldo_inicial' in attrs:
            if not isinstance(attrs['saldo_inicial'], numbers.Number):
                raise serializers.ValidationError("É necessário indicar o saldo inicial da conta.")
        else:
            raise serializers.ValidationError("É necessário indicar o saldo inicial da conta.")
        return attrs

    def create(self, validated_data):
        conta = Conta(**validated_data)
        conta.conta_categoria = False
        conta.save()
        return conta

    class Meta:
        model = Conta
        fields = ('pk', 'data_inicial', 'saldo_inicial', 'saldo_atual', 'nome', 'proprietario')
        extra_kwargs = {'proprietario': {'write_only': True}}


class CategoriaSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if 'data_inicial' in attrs:
            raise serializers.ValidationError("Uma categoria não deve ter data inicial.")
        if 'saldo_inicial' in attrs:
            raise serializers.ValidationError("Uma categoria não deve ter saldo inicial")
        return attrs
    
    def create(self, validated_data):
        categoria = Conta(**validated_data)
        categoria.conta_categoria = True
        categoria.save()
        return categoria

    class Meta:
        model = Conta
        fields = ('pk', 'nome', 'proprietario')
        extra_kwargs = {'proprietario': {'write_only': True}}


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('pk', 'tipo', 'data', 'conta_debito', 'conta_credito',
                  'valor', 'periodicidade', 'tempo_indeterminado', 'parcela_inicial',
                  'qtde_parcelas', 'ultima_atualizacao', 'proprietario')
        extra_kwargs = {'proprietario': {'write_only': True}}


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
        fields = ('pk', 'journal', 'data', 'conta_debito', 'conta_credito', 'valor', 'num_parcela', 'proprietario')
        extra_kwargs = {'proprietario': {'write_only': True}}
