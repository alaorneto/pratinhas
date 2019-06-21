""" Testes do módulo lançamentos. """
from datetime import datetime
from django.contrib.auth.models import User
from lancamentos.models import Conta, Journal, Lancamento
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

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

class JournalTestCase(APITestCase):
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