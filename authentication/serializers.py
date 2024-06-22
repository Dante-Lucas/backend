from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'telefone')

    def validate(self, data):
        print(data)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirm = data.get('confirmPassword')
        telefone = data.get('telefone')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already exists'}) 
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            telefone=validated_data['telefone']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()