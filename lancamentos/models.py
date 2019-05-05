"""
Modelos relacionados aos lançamentos (débitos e créditos).
"""
from django.db import models
from django.contrib.auth import get_user_model


class ProprietarioManager(models.Manager):
    """ Manager destinado a prover o filtro de entidades por proprietário. """

    def proprietario(self, usuario):
        """ Filtra o queryset por proprietário. """
        return super().get_queryset().filter(proprietario=usuario)


class Conta(models.Model):
    """ Contas agrupam lançamentos e mantêm um saldo corrente. """
    data_inicial = models.DateField()
    saldo_inicial = models.DecimalField(max_digits=9, decimal_places=2)
    nome = models.CharField(max_length=100)
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


class Categoria(models.Model):
    """ Representa um tipo de lançamento, com o objetivo de agrupar lançamentos do mesmo tipo. """
    nome = models.CharField(max_length=100)
    proprietario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()
    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


class Journal(models.Model):
    """ O journal tem a função de agrupar lançamentos que se repetem no tempo,
    guardando as características gerais desses itens. """
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    proprietario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()
    class Meta:
        verbose_name = "journal"
        verbose_name_plural = "journals"


class Lancamento(models.Model):
    """ É o nível mais atômico, representando um débito ou crédito em uma determiada conta. """
    data = models.DateField()
    valor = models.DecimalField(max_digits=9, decimal_places=2)
    proprietario = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    objects = ProprietarioManager()
    class Meta:
        verbose_name = "lançamento"
        verbose_name_plural = "lançamentos"
