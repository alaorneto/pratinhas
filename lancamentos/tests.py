""" Testes do módulo lançamentos. """
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

class ContaTestCase(APITestCase):
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

    def test_criar_conta(self):
        conta = {
            "data_inicial": datetime.now().date(),
            "saldo_inicial": 0.0,
            "nome": "Banco do Brasil",
        }
        response = self.client.post("/api/core/contas/", conta, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.json())
