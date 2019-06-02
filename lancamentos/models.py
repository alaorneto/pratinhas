"""
Modelos relacionados aos lançamentos (débitos e créditos).
"""
from django.db import models
from django.contrib.auth import get_user_model
import datetime
from dateutil import relativedelta

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
        get_user_model(),
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()

    def __str__(self):
        return self.nome
        
    class Meta:
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
    conta_debito = models.ForeignKey(Conta, related_name='journal_debitos', on_delete=models.CASCADE)
    conta_credito = models.ForeignKey(Conta, related_name='journal_creditos', on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    periodicidade = models.CharField(
        max_length=3, choices=PERIODICIDADE_CHOICES, default=UNICO
    )
    tempo_indeterminado = models.BooleanField()
    qtde_parcelas = models.IntegerField()
    ultima_atualizacao = models.DateTimeField()
    proprietario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()

    def categoria(self):
        if self.tipo == DEBITO:
            return conta_credito
        elif self.tipo == CREDITO:
            return conta_debito
        else:
            return None

    def preparar(self):
        pass

    def atualizar(self, data_atualizacao):
        if self.tempo_indeterminado is not True:
            return
        if not isinstance(data_atualizacao, datetime.datetime):
            raise TypeError("Espera-se uma data alvo, do tipo datetime, como argumento para atualização do journal.")

        data_inicial = self.ultima_atualizacao
        data_lancamento = self.data
        delta_count = 0

        while data_lancamento <= self.data_atualizacao:
            if data_lancamento <= data_inicial:
                continue
            lancamento = criar_lancamento(journal, data_lancamento)
            lancamento.save()
            self.ultima_atualizacao = data_lancamento
            self.save()
            delta_count += 1
            data_lancamento += self.data + __obter_delta(self, delta_count)


    def __obter_delta(self, journal, delta=1):
        if journal.periodicidade == "SEM":
            return relativedelta.relativedelta(weeks=+delta)
        elif journal.periodicidade == "MES":
            return relativedelta.relativedelta(months=+delta)
        elif journal.periodicidade == "ANO":
            return relativedelta.relativedelta(years=+delta)
        else:
            return relativedelta.relativedelta(days=0)


    class Meta:
        verbose_name = "journal"
        verbose_name_plural = "journals"


class Lancamento(models.Model):
    """ É o nível mais atômico, representando um débito ou crédito em uma determiada conta. """
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
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    num_parcela = models.IntegerField()
    proprietario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()

    def categoria(self):
        if self.tipo == DEBITO:
            return conta_credito
        elif self.tipo == CREDITO:
            return conta_debito
        else:
            return None

    class Meta:
        verbose_name = "lançamento"
        verbose_name_plural = "lançamentos"
