from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


class LogoutAPIView(APIView):
    def post(self, request:Request) -> Response:
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