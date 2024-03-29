"""
Modelos relacionados aos lançamentos (débitos e créditos).
"""
import datetime
from decimal import Decimal
from dateutil import relativedelta
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.conf import settings


class ProprietarioManager(models.Manager):
    """ Manager destinado a prover o filtro de entidades por proprietário. """

    def proprietario(self, usuario):
        """ Filtra o queryset por proprietário. """
        return super().get_queryset().filter(proprietario=usuario)


class Conta(models.Model):
    """ Contas agrupam lançamentos e mantêm um saldo corrente. """
    data_inicial = models.DateField(null=True)
    saldo_inicial = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    nome = models.CharField(max_length=100)
    conta_categoria = models.BooleanField()
    proprietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()

    @property
    def saldo_atual(self):
        data_atual = datetime.datetime.now().date()
        creditos = Lancamento.objects.filter(conta_credito__nome=self.nome, conta_credito__proprietario=self.proprietario, data__lte=data_atual).aggregate(sum_credito=Coalesce(Sum('valor'), Decimal(0)))
        debitos = Lancamento.objects.filter(conta_debito__nome=self.nome, conta_debito__proprietario=self.proprietario, data__lte=data_atual).aggregate(sum_debito=Coalesce(Sum('valor'), Decimal(0)))

        saldo_atual = self.saldo_inicial + creditos['sum_credito'] - debitos['sum_debito']

        return saldo_atual
    

    def saldo_em(self, data_alvo):
        creditos = Lancamento.objects.filter(conta_credito__nome=self.nome, conta_credito__proprietario=self.proprietario, data__lte=data_alvo).aggregate(sum_credito=Coalesce(Sum('valor'), Decimal(0)))
        debitos = Lancamento.objects.filter(conta_debito__nome=self.nome, conta_debito__proprietario=self.proprietario, data__lte=data_alvo).aggregate(sum_debito=Coalesce(Sum('valor'), Decimal(0)))

        saldo_atual = self.saldo_inicial + creditos['sum_credito'] - debitos['sum_debito']

        return saldo_atual

    def __str__(self):
        return self.nome

    class Meta:
        app_label = 'lancamentos'
        verbose_name = "conta"
        verbose_name_plural = "contas"
        unique_together = ['nome', 'proprietario']


class Journal(models.Model):
    """ O journal tem a função de agrupar lançamentos que se repetem no tempo,
    guardando as características gerais desses itens. """
    DEBITO = 'DBT'
    CREDITO = 'CRD'
    TRANSFERENCIA = 'TRF'
    TIPO_CHOICES = (
        (DEBITO, 'Débito'),
        (CREDITO, 'Crédito'),
        (TRANSFERENCIA, 'Transferência'),
    )
    UNICO = 'UNI'
    SEMANAL = 'SEM'
    MENSAL = 'MES'
    ANUAL = 'ANO'
    PERIODICIDADE_CHOICES = (
        (UNICO, 'Único'),
        (SEMANAL, 'Semanal'),
        (MENSAL, 'Mensal'),
        (ANUAL, 'Anual'),
    )
    tipo = models.CharField(
        max_length=3, choices=TIPO_CHOICES, default=DEBITO)
    data = models.DateField()
    conta_debito = models.ForeignKey(Conta, related_name='journal_debitos',
                                     on_delete=models.CASCADE)
    conta_credito = models.ForeignKey(Conta, related_name='journal_creditos',
                                      on_delete=models.CASCADE)
    descricao = models.TextField(max_length=250)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    periodicidade = models.CharField(
        max_length=3, choices=PERIODICIDADE_CHOICES, default=UNICO
    )
    tempo_indeterminado = models.BooleanField()
    parcela_inicial = models.IntegerField(null=True)
    qtde_parcelas = models.IntegerField(null=True)
    ultima_atualizacao = models.DateField(null=True)
    proprietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()

    def categoria(self):
        """ Retorna a conta correspondente a categoria do lançamento. """
        if self.tipo == self.DEBITO:
            return self.conta_credito
        elif self.tipo == self.CREDITO:
            return self.conta_debito
        else:
            return None

    def _inicializar(self):
        """ Cria os lançamentos de um determinado journal. """

        if self.ultima_atualizacao:
            raise Exception("O journal já foi inicializado anteriormente.")

        data_atualizacao = datetime.datetime.now().date()

        # O journal possui repetição de lançamentos (periodicidade)
        if self.tempo_indeterminado is False and self.periodicidade != Journal.UNICO:
            num_parcela = self.parcela_inicial
            data_lancamento = self.data
            while num_parcela <= self.qtde_parcelas:
                lancamento = self._criar_lancamento(data_lancamento, num_parcela)
                lancamento.save()
                num_parcela += 1
                data_lancamento = self.data + self._obter_delta(
                    num_parcela - self.parcela_inicial)
            data_atualizacao = data_lancamento


        # O journal possui apenas um lançamento (único)
        if (self.tempo_indeterminado is False and self.periodicidade == Journal.UNICO) or (self.tempo_indeterminado):
            lancamento = self._criar_lancamento(self.data)
            lancamento.save()
            data_atualizacao = self.data

        self.ultima_atualizacao = data_atualizacao
        self.save()

    def atualizar(self, data_atualizacao):
        """ Cria os lançamentos de um journal até determinada data. """
        if self.tempo_indeterminado is not True:
            raise Exception("Este journal não é do tipo 'tempo indeterminado', logo, não pode ser atualizado.")
        if self.pk is None:
            raise Exception("O journal precisa estar salvo para ser atualizado.")
        if not isinstance(data_atualizacao, datetime.date):
            raise TypeError("Espera-se uma data alvo, do tipo datetime, " +
                            "como argumento para atualização do journal.")

        data_inicial = self.ultima_atualizacao
        data_lancamento = self.data
        delta_count = 0

        while data_lancamento <= data_atualizacao:
            if data_lancamento > data_inicial:
                lancamento = self._criar_lancamento(data_lancamento)
                lancamento.save()
            delta_count += 1
            data_lancamento = self.data + self._obter_delta(delta_count)

        self.ultima_atualizacao = data_atualizacao
        self.save()

    def _criar_lancamento(self, data_lancamento, num_parcela=0):
        """ Cria um lançamento baseado nos dados de um journal. """
        lancamento = Lancamento(journal=self,
                                data=data_lancamento,
                                conta_debito=self.conta_debito,
                                conta_credito=self.conta_credito,
                                valor=self.valor,
                                num_parcela=num_parcela,
                                proprietario=self.proprietario)
        return lancamento

    def _obter_delta(self, delta=1):
        if self.periodicidade == "SEM":
            return relativedelta.relativedelta(weeks=+delta)
        elif self.periodicidade == "MES":
            return relativedelta.relativedelta(months=+delta)
        elif self.periodicidade == "ANO":
            return relativedelta.relativedelta(years=+delta)
        else:
            return relativedelta.relativedelta(days=0)

    def save(self, *args, **kwargs):
        """ Ao salvar, inicializar o Journal se for o momento da criação. """
        if not self.id:
            super(Journal, self).save(*args, **kwargs)
            self._inicializar()
        else:
            return super(Journal, self).save(*args, **kwargs)

    class Meta:
        app_label = 'lancamentos'
        verbose_name = "journal"
        verbose_name_plural = "journals"


class Lancamento(models.Model):
    """ É o nível mais atômico, representando um débito, crédito
    ou uma transferência entre contas. """
    DEBITO = 'DBT'
    CREDITO = 'CRD'
    TRANSFERENCIA = 'TRF'
    TIPO_CHOICES = (
        (DEBITO, 'Débito'),
        (CREDITO, 'Crédito'),
        (TRANSFERENCIA, 'Transferência'),
    )
    journal = models.ForeignKey(
        'lancamentos.Journal', on_delete=models.CASCADE)
    data = models.DateField()
    conta_debito = models.ForeignKey(
        Conta, related_name='debitos', on_delete=models.CASCADE)
    conta_credito = models.ForeignKey(
        Conta, related_name='creditos', on_delete=models.CASCADE)
    descricao = models.TextField(max_length=250)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    num_parcela = models.IntegerField()
    proprietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()

    def categoria(self):
        """ Retorna a categoria do lançamento. """
        return self.journal.categoria()

    class Meta:
        app_label = 'lancamentos'
        verbose_name = "lançamento"
        verbose_name_plural = "lançamentos"
