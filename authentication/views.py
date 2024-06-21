from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
from .models import User
from .serializers import UserSerializer,LoginSerializer
# Create your views here.

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def post(self, request:Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(): 
            try:
                serializer.save()    
                return Response({'success': 'Usuário criado com sucesso'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'Erro ao criar o usuário'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request:Request) -> Response:
        return Response({'detail': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def post(self, request:Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                csrf_token = get_token(request)
                return Response({'success': 'Logado com sucesso', 'csrf_token': csrf_token}, status=status.HTTP_200_OK)
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request:Request) -> Response:
        return Response({'detail': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    def post(self,request:Request) -> Response:
            auth.logout(request)
            return Response({'success':'Deslogado com sucesso'}, status=status.HTTP_200_OK)