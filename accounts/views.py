from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UsuarioSerializer

class RegisterView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (AllowAny, )

class AccountView(APIView):
    def post(self, request):
        pass

class UsuarioViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = UsuarioSerializer