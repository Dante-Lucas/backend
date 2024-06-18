from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer,LoginSerializer
# Create your views here.

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            data_nascimento = serializer.validated_data.get('data_nascimento')
            users = User.objects.filter(username=username,email=email)
            if users.exists():
                return Response({'error':'Usuário ja existe'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password,
                                                data_nascimento=data_nascimento)
                
            except IntegrityError:
                return Response({'error':'Error criar o usuário'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'Sucess':'Usuário criado com sucesso'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'detail': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
@api_view(['GET','POST']) 
@permission_classes([AllowAny])       
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return Response({'Sucess':'Logado com sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Credenciais inválidas'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([AllowAny])
def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return Response({'Sucess':'Deslogado com sucesso'}, status=status.HTTP_200_OK)