from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import permission_required,login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import constants
from django.contrib import messages 
from django.urls import reverse
from rest_framework.views import APIView
from django.utils.decorators import method_decorator 
from django.db import transaction,IntegrityError
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
from rest_framework.permissions import IsAuthenticated,AllowAny
from authentication.models import User
from ..serializers import CategoriaSerializer
from ..models import Categoria

class CategoriaView(APIView):

    def get_objects_all(self):
        return Categoria.objects.all()
    def get(self, request):
        categoria = self.get_objects_all()

        serializer = CategoriaSerializer(categoria, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request:Request) -> Response:
        
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categorias = serializer.validated_data.get('nome')
        try:

            categoria = Categoria.objects.create(nome=categorias)
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except Exception:
             return Response({"error": "Erro ao cadastrar a categoria."},status=status.HTTP_400_BAD_REQUEST)