from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

class ContaTestCase(APITestCase):
    client = APIClient()
    user = None
    token = None

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@pratinhas.app', 'Test1234!')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login(self):
        self.assertTrue(self.client.login(username='test', password='Test1234!'))

    def test_token(self):
        response = self.client.get('/api/core/usuarios/')
        self.assertEqual(response.status_code, 200)

    def test_criar_conta(self):
        pass