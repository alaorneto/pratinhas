""" Testes do módulo lançamentos. """
from datetime import datetime
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.renderers import JSONRenderer

from lancamentos.models import Conta, Journal, Lancamento
from .serializers import LancamentoSerializer


class ContaTestCase(APITestCase):
    """ Testes de operações com contas. """
    client = None
    user = None
    username = 'test'
    email = 'test@pratinhas.app'
    password = 'Test1234!'

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_criar_contas(self):
        bb = {
            "data_inicial": datetime.now().date(),
            "saldo_inicial": 0.0,
            "nome": "Banco do Brasil",
        }
        response = self.client.post("/api/core/contas/", bb, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cef = {
            "data_inicial": datetime.now().date(),
            "saldo_inicial": 155.0,
            "nome": "Caixa Econômica Federal",
        }
        response = self.client.post("/api/core/contas/", cef, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Conta.objects.proprietario(self.user).count(), 2)

    def test_criar_conta_sem_data_inicial(self):
        conta = {
            "saldo_inicial": 10.55,
            "nome": "Santander",
        }
        response = self.client.post("/api/core/contas/", conta, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_conta_sem_saldo_inicial(self):
        conta = {
            "data_inicial": datetime.now().date(),
            "nome": "Santander",
        }
        response = self.client.post("/api/core/contas/", conta, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_conta_sem_nome(self):
        conta = {
            "data_inicial": datetime.now().date(),
            "saldo_inicial": 113.47,
        }
        response = self.client.post("/api/core/contas/", conta, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_conta_sem_autenticacao(self):
        client_sem_autenticacao = APIClient()
        conta = {
            "data_inicial": datetime.now().date(),
            "saldo_inicial": 12.80,
            "nome": "Santander",
        }
        response = client_sem_autenticacao.post("/api/core/contas/", conta, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoriaTestCase(APITestCase):
    """ Testes de operações com contas. """
    client = None
    user = None
    username = 'test'
    email = 'test@pratinhas.app'
    password = 'Test1234!'

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_criar_categorias(self):
        alimentacao = {
            "nome": "Alimentação",
        }
        response = self.client.post("/api/core/categorias/", alimentacao, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        vestuario = {
            "nome": "Vestuário",
        }
        response = self.client.post("/api/core/categorias/", vestuario, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Conta.objects.proprietario(self.user).filter(conta_categoria=True).count(), 2)


class LancamentoTestCase(APITestCase):
    """ Testes de operações com contas. """
    client = None
    user = None
    username = 'test'
    email = 'test@pratinhas.app'
    password = 'Test1234!'

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
                
        bb = {
            "data_inicial": datetime.now().date(),
            "saldo_inicial": 0.0,
            "nome": "Banco do Brasil",
        }
        response = self.client.post("/api/core/contas/", bb, format='json')

        cef = {
            "data_inicial": datetime.now().date(),
            "saldo_inicial": 155.0,
            "nome": "Caixa Econômica Federal",
        }
        response = self.client.post("/api/core/contas/", cef, format='json')

        alimentacao = {
            "nome": "Alimentação",
        }
        response = self.client.post("/api/core/categorias/", alimentacao, format='json')

        vestuario = {
            "nome": "Vestuário",
        }
        response = self.client.post("/api/core/categorias/", vestuario, format='json')

        self.assertEqual(Conta.objects.proprietario(self.user).filter(conta_categoria=False).count(), 2)
        self.assertEqual(Conta.objects.proprietario(self.user).filter(conta_categoria=True).count(), 2)
    
    def test_criar_journal_unico(self):
        conta = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Banco do Brasil")
        categoria = Conta.objects.proprietario(self.user).filter(conta_categoria=True).get(nome="Alimentação")
        journal = {
            "tipo": Journal.CREDITO,
            "data": datetime.now().date(),
            "conta_debito": conta.pk,
            "conta_credito": categoria.pk,
            "valor": 1000.00,
            "periodicidade": Journal.UNICO,
            "tempo_indeterminado": False,
            "parcela_inicial": 0,
            "qtde_parcelas": 0,
        }
        response = self.client.post("/api/core/lancamentos/", journal, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.proprietario(self.user).count(), 1)
        self.assertEqual(Lancamento.objects.proprietario(self.user).count(), 1)

    def test_criar_journal_periodico(self):
        conta = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Banco do Brasil")
        categoria = Conta.objects.proprietario(self.user).filter(conta_categoria=True).get(nome="Alimentação")
        journal = {
            "tipo": Journal.CREDITO,
            "data": datetime(2020, 1, 31).date(),
            "conta_debito": conta.pk,
            "conta_credito": categoria.pk,
            "valor": 1000.00,
            "periodicidade": Journal.MENSAL,
            "tempo_indeterminado": False,
            "parcela_inicial": 2,
            "qtde_parcelas": 5,
        }
        response = self.client.post("/api/core/lancamentos/", journal, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.proprietario(self.user).count(), 1)
        self.assertEqual(Lancamento.objects.proprietario(self.user).count(), 4)
    
    def test_criar_journal_tempo_indeterminado(self):
        conta = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Banco do Brasil")
        categoria = Conta.objects.proprietario(self.user).filter(conta_categoria=True).get(nome="Alimentação")
        journal = {
            "tipo": Journal.CREDITO,
            "data": datetime(2020, 1, 31).date(),
            "conta_debito": conta.pk,
            "conta_credito": categoria.pk,
            "valor": 1000.00,
            "periodicidade": Journal.MENSAL,
            "tempo_indeterminado": True,
        }
        response = self.client.post("/api/core/lancamentos/", journal, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.proprietario(self.user).count(), 1)
        self.assertEqual(Lancamento.objects.proprietario(self.user).count(), 1)

        journals = Journal.objects.proprietario(self.user).all()
        for journal in journals:
            journal.atualizar(datetime(2021,4,20).date())
        self.assertEqual(Lancamento.objects.proprietario(self.user).count(), 15)

        journals = Journal.objects.proprietario(self.user).all()
        for journal in journals:
            journal.atualizar(datetime(2021,5,31).date())
        self.assertEqual(Lancamento.objects.proprietario(self.user).count(), 17)
    
    def test_alterar_valor_lancamento(self):
        conta = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Banco do Brasil")
        categoria = Conta.objects.proprietario(self.user).filter(conta_categoria=True).get(nome="Alimentação")
        journal = {
            "tipo": Journal.CREDITO,
            "data": datetime(2020, 2, 20).date(),
            "conta_debito": conta.pk,
            "conta_credito": categoria.pk,
            "valor": 5000.00,
            "periodicidade": Journal.MENSAL,
            "tempo_indeterminado": True,
        }
        response = self.client.post("/api/core/lancamentos/", journal, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.proprietario(self.user).count(), 1)

        journals = Journal.objects.proprietario(self.user).all()
        for journal in journals:
            journal.atualizar(datetime(2021,4,30).date())
        
        lancamento = get_object_or_404(Lancamento.objects.proprietario(self.user), data=datetime(2020, 2, 20).date())
        self.assertEqual(lancamento.valor, 5000)
        lancamento.valor = 533.33
        serializer = LancamentoSerializer(lancamento)
        response = self.client.put(f"/api/core/lancamentos/{lancamento.pk}/", serializer.data, format='json')
        lancamento = get_object_or_404(Lancamento.objects.proprietario(self.user), data=datetime(2020, 2, 20).date())
        self.assertNotEqual(lancamento.valor, 5000)

    
    def test_alterar_valor_lancamento_e_futuros(self):
        conta_bb = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Banco do Brasil")
        categoria = Conta.objects.proprietario(self.user).filter(conta_categoria=True).get(nome="Alimentação")
        journal = {
            "tipo": Journal.CREDITO,
            "data": datetime(2020, 2, 20).date(),
            "conta_debito": conta_bb.pk,
            "conta_credito": categoria.pk,
            "valor": 5000.00,
            "periodicidade": Journal.MENSAL,
            "tempo_indeterminado": True,
        }
        response = self.client.post("/api/core/lancamentos/", journal, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.proprietario(self.user).count(), 1)

        journals = Journal.objects.proprietario(self.user).all()
        for journal in journals:
            journal.atualizar(datetime(2021,4,30).date())
        
        lancamento = get_object_or_404(Lancamento.objects.proprietario(self.user), data=datetime(2020, 2, 20).date())
        journal_id = lancamento.journal_id
        self.assertEqual(lancamento.conta_debito.nome, 'Banco do Brasil')
        lancamento.valor = 355.78
        serializer = LancamentoSerializer(lancamento)
        data = serializer.data
        data['futuros'] = True
        response = self.client.put(f"/api/core/lancamentos/{lancamento.pk}/", data, format='json')
        lancamentos = Lancamento.objects.proprietario(self.user).filter(journal_id=journal_id)
        
        for lancamento in lancamentos:
            self.assertNotEqual(lancamento.valor, 5000.00)

    def test_alterar_conta_lancamento(self):
        conta_bb = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Banco do Brasil")
        conta_cef = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Caixa Econômica Federal")
        categoria = Conta.objects.proprietario(self.user).filter(conta_categoria=True).get(nome="Alimentação")
        journal = {
            "tipo": Journal.CREDITO,
            "data": datetime(2020, 2, 20).date(),
            "conta_debito": conta_bb.pk,
            "conta_credito": categoria.pk,
            "valor": 5000.00,
            "periodicidade": Journal.MENSAL,
            "tempo_indeterminado": True,
        }
        response = self.client.post("/api/core/lancamentos/", journal, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.proprietario(self.user).count(), 1)

        journals = Journal.objects.proprietario(self.user).all()
        for journal in journals:
            journal.atualizar(datetime(2021,4,30).date())
        
        lancamento = get_object_or_404(Lancamento.objects.proprietario(self.user), data=datetime(2020, 2, 20).date())
        self.assertEqual(lancamento.conta_debito.nome, 'Banco do Brasil')
        lancamento.conta_debito = conta_cef
        serializer = LancamentoSerializer(lancamento)
        response = self.client.put(f"/api/core/lancamentos/{lancamento.pk}/", serializer.data, format='json')
        lancamento = get_object_or_404(Lancamento.objects.proprietario(self.user), data=datetime(2020, 2, 20).date())
        self.assertNotEqual(lancamento.conta_debito.nome, 'Banco do Brasil')

    def test_alterar_conta_lancamento_e_futuros(self):
        conta_bb = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Banco do Brasil")
        conta_cef = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Caixa Econômica Federal")
        categoria = Conta.objects.proprietario(self.user).filter(conta_categoria=True).get(nome="Alimentação")
        journal = {
            "tipo": Journal.CREDITO,
            "data": datetime(2020, 2, 20).date(),
            "conta_debito": conta_bb.pk,
            "conta_credito": categoria.pk,
            "valor": 5000.00,
            "periodicidade": Journal.MENSAL,
            "tempo_indeterminado": True,
        }
        response = self.client.post("/api/core/lancamentos/", journal, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journal.objects.proprietario(self.user).count(), 1)

        journals = Journal.objects.proprietario(self.user).all()
        for journal in journals:
            journal.atualizar(datetime(2021,4,30).date())
        
        lancamento = get_object_or_404(Lancamento.objects.proprietario(self.user), data=datetime(2020, 2, 20).date())
        journal_id = lancamento.journal_id
        self.assertEqual(lancamento.conta_debito.nome, 'Banco do Brasil')
        lancamento.conta_debito = conta_cef
        serializer = LancamentoSerializer(lancamento)
        data = serializer.data
        data['futuros'] = True
        response = self.client.put(f"/api/core/lancamentos/{lancamento.pk}/", data, format='json')
        lancamentos = Lancamento.objects.proprietario(self.user).filter(journal_id=journal_id)
        
        for lancamento in lancamentos:
            self.assertNotEqual(lancamento.conta_debito.nome, 'Banco do Brasil')
    
    def test_excluir_lancamento_unico(self):
        conta = Conta.objects.proprietario(self.user).filter(conta_categoria=False).get(nome="Banco do Brasil")
        categoria = Conta.objects.proprietario(self.user).filter(conta_categoria=True).get(nome="Alimentação")
        journal = {
            "tipo": Journal.CREDITO,
            "data": datetime.now().date(),
            "conta_debito": conta.pk,
            "conta_credito": categoria.pk,
            "valor": 1012.21,
            "periodicidade": Journal.UNICO,
            "tempo_indeterminado": False,
        }
        response = self.client.post("/api/core/lancamentos/", journal, format='json')
        lancamento = get_object_or_404(Lancamento.objects.proprietario(self.user), valor=1012.21)
        self.assertEqual(Lancamento.objects.proprietario(self.user).filter(valor=1012.21).count(), 1)
        response = self.client.delete(f"/api/core/lancamentos/{lancamento.pk}/")
        self.assertEqual(Lancamento.objects.proprietario(self.user).filter(valor=1012.21).count(), 0)