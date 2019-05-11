from django import forms


class ContaForm(forms.Form):
    nome = forms.CharField(label="Nome da conta", max_length=100)
    data_inicial = forms.DateField(label="Data inicial da conta")
    saldo_inicial = forms.DecimalField(label="Saldo inicial da conta", max_digits=9 decimal_places=2)