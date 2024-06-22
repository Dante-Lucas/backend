from rest_framework import serializers
from .models import Produto,Fabricante,Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class FabricanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricante
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    fabricante = serializers.CharField(write_only=True)
    categoria = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Produto
        fields = ['id', 'nome_produto', 'descricao', 'preco', 'estoque', 'fabricante', 'categoria']

    def create(self, validated_data):
        fabricante = validated_data.pop('fabricante')
        categoria = validated_data.pop('categoria', None)

        try:
            fabricantes,created = Fabricante.objects.get_or_create(nome=fabricante)
        except Fabricante.DoesNotExist:
            raise serializers.ValidationError('Fabricante não encontrado')
        
        categorias =None
        try:
            cate, created = Categoria.objects.get_or_create(nome=cate)
        except Categoria.DoesNotExist:
            raise serializers.ValidationError('Categoria não encontrada')
        produto = Produto.objects.create(fabricante=fabricantes, categoria=cate, **validated_data) 
        return produto