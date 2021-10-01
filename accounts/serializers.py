from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}