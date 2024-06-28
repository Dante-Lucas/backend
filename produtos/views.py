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
from .serializers import ProdutoSerializer,CategoriaSerializer,FabricanteSerializer
from .models import Produto,Categoria,Fabricante
# Create your views here.
messages.success
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
        

#@method_decorator([csrf_exempt],name='dispatch')
class CategoriaView(APIView):

    def get_objects_all(self):
        return Categoria.objects.all()
    def get(self, request):
        categoria = self.get_objects_all()

        serializer = FabricanteSerializer(categoria, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request:Request) -> Response:
        
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categorias = serializer.validated_data.get('nome')
        try:

            categoria = Categoria.objects.create(nome=categorias)
            
            return Response({"success": "Categoria cadastrada com sucesso!"},serializer.data,status=status.HTTP_201_CREATED)
        except Exception:
             return Response({"error": "Erro ao cadastrar a categoria."},status=status.HTTP_400_BAD_REQUEST)



class FabricanteView(APIView):
    def get_objects_all(self):
        return Fabricante.objects.all()
    def get(self, request):
        fabricante = self.get_objects_all()

        serializer = FabricanteSerializer(fabricante, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer,BrowsableAPIRenderer]
    def get(self,request:Request) -> Response:
        produtos = Produto.objects.all()

        serializer = ProdutoSerializer(produtos, many=True)
        #list_produtos = []
#
        #for produto in produtos:
        #    categoria = Categoria.objects.get(id=produto.categoria.pk)
        #    fabricante = Fabricante.objects.get(id=produto.fabricante.pk)
        #    
        #    data = {
        #        'id': produto.pk,
        #        'nome_produto': produto.nome_produto,
        #        'descricao': produto.descricao,
        #        'preco': produto.preco,
        #        'estoque': produto.nome_produto,
        #        'fabricante': None,
        #        'categoria': None,
        #    }
        #    outhers_data = {
        #        'dados_fabricante': {
        #            'id': fabricante.pk,
        #            'nome': fabricante.nome,
        #        },
        #        'dados_categoria': {
        #            'id': categoria.pk,
        #            'nome': categoria.nome,
        #        },
        #    }
        #    data["fabricante"] = outhers_data["dados_fabricante"]
        #    data["categoria"] = outhers_data["dados_categoria"]
        #    list_produtos.append(data)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({'menssage':'Nenhum produto encontrado'},status=status.HTTP_404_NOT_FOUND)
    def post(self, request: Request) -> Response:
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({'message': f'Erro ao enviar o cadastro. motivo {e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
class ProdutoDetailsView(APIView):
    def get(self,request,id):
        produto = get_object_or_404(Produto,id=id)
        serializer = ProdutoSerializer(produto) 
        if serializer is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "error"})


    def put(self,request:Request,id) -> Response:
        
        produto = get_object_or_404(Produto,id=id)
        serializer = ProdutoSerializer(produto,data=request.data)
        if serializer.is_valid():
            response = ProdutoSerializer(serializer.save())
            return Response(response.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request:Request,id) -> Response:
        produto = get_object_or_404(Produto,id=id)
        produto.delete()
        return Response({'message':'Produto deletado com sucesso!'},status=status.HTTP_204_NO_CONTENT)
        
