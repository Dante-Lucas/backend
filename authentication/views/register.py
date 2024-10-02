from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.db import IntegrityError
from ..serializers import UserSerializer


class RegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = UserSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'success': 'Usuário criado com sucesso'},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError:
            return Response(
                {'error': 'Erro ao criar o usuário'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(
            {'detail': 'Método não permitido'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
