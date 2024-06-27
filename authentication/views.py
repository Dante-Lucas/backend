from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,logout
from django.urls import reverse
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
from .models import User
from .serializers import UserSerializer,LoginSerializer
# Create your views here.

class RegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserSerializer

    def post(self, request:Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'success': 'Usuário criado com sucesso'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'error': 'Erro ao criar o usuário'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request:Request, *args, **kwargs) -> Response:
        return Response({'detail': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    def post(self, request:Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({'success': 'Logado com sucesso', 'token':token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request:Request) -> Response:
        return Response({'detail': 'Método não permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            # Obtém o token do cabeçalho Authorization
            token_key = request.headers.get('Authorization').split(' ')[1]
            # Encontra o token correspondente no banco de dados
            token = Token.objects.get(key=token_key)
            # Invalida o token (remove-o do banco de dados)
            token.delete()
            return Response(status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'detail': 'Token não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)