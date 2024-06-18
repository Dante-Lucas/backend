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
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from .serializers import ProdutoSerializer,CategoriaSerializer,FabricanteSerializer
from .models import Produto,Categoria,Fabricante
# Create your views here.

class ProdutoListView(APIView):
   permission_classes = [IsAuthenticated]
   parser_classes = [JSONParser]
   def get(self,request:Request) -> Response:
        fabricante = request.query_params.get('fabricante')
        categoria = request.query_params.get('categoria')
        produtos = Produto.objects.all()

        if categoria:
            produtos = produtos.filter(categoria_id=int(categoria))
            
        if fabricante:
            produtos = produtos.filter(fabricante_id=int(fabricante))
        
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)
        

@method_decorator([csrf_exempt],name='dispatch')
class CategoriaView(APIView):
    def post(self,request:Request) -> Response:
        
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categorias = serializer.validated_data.get('nome')
        try:

            categoria = Categoria.objects.create(nome=categorias)
            
            return Response({"success": "Categoria cadastrada com sucesso!"},serializer.data,status=status.HTTP_201_CREATED)
        except Exception:
             return Response({"error": "Erro ao cadastrar a categoria."},status=status.HTTP_400_BAD_REQUEST)


@method_decorator([csrf_exempt],name='dispatch')
class FabricanteView(APIView):
    def post(self,request:Request) -> Response:
        
        serialiazer = FabricanteSerializer(data=request.data)
        if serialiazer.is_valid():
            fabricantes = serialiazer.validated_data.get('nome')
        try:
            fabricante=Fabricante.objects.create(nome=fabricantes)

            return Response({'message':'Fabricante adicionado com sucesso!'})
        except Exception as e:
            return Response({'error':'Erro ao casdatrar o fabricante.'},status=status.HTTP_400_BAD_REQUEST)
        


class ProdutoView(APIView):
    
    def get(self,request:Request) -> Response:
        produto = Produto.objects.all() 
        if produto is not None:
            serializer = ProdutoSerializer(produto,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'menssage':'Nenhum produto encontrado'},status=status.HTTP_404_NOT_FOUND)
   
    def post(self,request:Request) -> Response:
        serializer=ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            nome_produto=serializer.validated_data.get('nome_produto')
            descricao=serializer.validated_data.get('descricao')
            preco=serializer.validated_data.get('preco')                        
            quantidade=serializer.validated_data.get('quantidade')
            fabricante=serializer.validated_data.get('fabricante')
            categoria=serializer.validated_data.get('categoria') 
        with transaction.atomic():
            try:
                fabricantes = Fabricante.objects.get(pk=fabricante)
                categorias = Categoria.objects.get(pk=categoria)
                
                produto = Produto(
                        user=request.user,
                        nome_produto=nome_produto,
                        descricao=descricao,
                        preco=preco,
                        estoque=quantidade,
                        fabricante=fabricantes,
                        categoria=categorias
                    )
                produto.save()
                return Response({'message-success':'Produto salvo com sucesso!'},serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'message':'Erro ao enviar o cadastro. motivo {e}'},status=status.HTTP_400_BAD_REQUEST)
            
class ProdutoDetailsView(APIView):
    def get(request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = ProdutoSerializer(produto) 
        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "error"})


    def put(request:Request,id) -> Response:
        
        produto = get_object_or_404(Produto,id=id)
        serializer = ProdutoSerializer(produto,data=request.data)
        
        serializer.save()
        
        return Response({'message':'Produto atualizado com sucesso!'},status=status.HTTP_200_OK)
        

    def delete(request:Request,id) -> Response:
        produto = get_object_or_404(Produto,id=id)
        produto.delete()
        return Response({'message':'Produto deletado com sucesso!'},status=status.HTTP_204_NO_CONTENT)
        
