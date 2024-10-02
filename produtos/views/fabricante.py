from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from ..serializers import FabricanteSerializer
from ..models import Fabricante


class FabricanteView(APIView):
    def get_objects_all(self):
        return Fabricante.objects.all()

    def get(self, request):
        fabricante = self.get_objects_all()

        serializer = FabricanteSerializer(fabricante, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serialiazer = FabricanteSerializer(data=request.data)
        if serialiazer.is_valid():
            fabricantes = serialiazer.validated_data.get('nome')
        try:
            fabricante = Fabricante.objects.create(nome=fabricantes)

            return Response(serialiazer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': 'Erro ao casdatrar o fabricante.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
