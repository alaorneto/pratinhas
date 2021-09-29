from django.conf import settings
from rest_framework import serializers

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('username', 'password', 'email', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}