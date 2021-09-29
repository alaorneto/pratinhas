from django.contrib import admin
from .models import Conta, Lancamento, Journal

admin.site.register(Conta)
admin.site.register(Lancamento)
admin.site.register(Journal)
