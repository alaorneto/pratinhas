""" Testes do módulo de autenticação. """
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


class UsuarioTestCase(APITestCase):
    """ Testes de operações com contas. """
    client = None
    user = None
    username = 'test'
    email = 'test@pratinhas.app'
    password = 'Test1234!'

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(self.username, self.email, self.password)
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post("/api/token/", payload, format='json')
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_registrar_usuario(self):
        usuario = {
            "username": 'alaor',
            "password": 'Test12#',
            "email": "test@test.com",
        }
        response = self.client.post("/api/accounts/register", usuario, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)