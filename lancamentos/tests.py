""" Testes do módulo lançamentos. """
from datetime import datetime
from django.contrib.auth.models import User
from lancamentos.models import Conta
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