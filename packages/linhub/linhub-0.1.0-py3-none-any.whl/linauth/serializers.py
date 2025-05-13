import hashlib

from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'avatar', 'date_joined', 'is_active')
        read_only_fields = ['is_active', 'date_joined']


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'created',)
