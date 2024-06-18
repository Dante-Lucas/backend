from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'data_nascimento')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()