from rest_framework import serializers
from ..models import Produto,Fabricante,Categoria
from . import FabricanteSerializer, CategoriaSerializer
class ProdutoSerializer(serializers.ModelSerializer):
    # O campo 'fabricante' é um campo de entrada que representa o nome do fabricante
    # O campo 'categoria' é um campo de entrada opcional que representa o nome da categoria
    fabricante = serializers.CharField(write_only=True)
    categoria = serializers.CharField(write_only=True, required=False)

    # Os campos 'dados_fabricante' e 'dados_categoria' são campos de saída que representam os dados do fabricante e da categoria
    # Respectivamente, eles são criados a partir dos campos 'fabricante' e 'categoria' usando os serializadores correspondentes
    dados_fabricante = FabricanteSerializer(read_only=True, source='fabricante')
    dados_categoria = CategoriaSerializer(read_only=True, source='categoria')

    class Meta:
        model = Produto
        fields = ['id', 'nome_produto', 'descricao', 'preco', 'estoque', 'fabricante', 'categoria', 'dados_fabricante', 'dados_categoria']

    def create(self, validated_data):
        # Obter o nome do fabricante a partir dos dados validados
        fabricante_nome = validated_data.pop('fabricante')

        # Obter o nome da categoria a partir dos dados validados (se fornecido)
        categoria_nome = validated_data.pop('categoria', None)

        # Obter ou criar o fabricante correspondente ao nome fornecido
        fabricante, created = Fabricante.objects.get_or_create(nome=fabricante_nome)

        # Obter ou criar a categoria correspondente ao nome fornecido (se fornecida)
        categoria = None
        if categoria_nome:
            categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)

        # Criar o novo produto com os dados fornecidos e os fabricante e categoria correspondentes
        produto = Produto.objects.create(fabricante=fabricante, categoria=categoria, **validated_data)

        return produto
    
    def update(self, instance, validated_data):
        # Obter o nome do fabricante a partir dos dados validados
        fabricante_nome = validated_data.pop('fabricante')
        categoria_nome = validated_data.pop('categoria', None)

        # Obter ou criar o fabricante correspondente ao nome fornecido
        fabricante, created = Fabricante.objects.get_or_create(nome=fabricante_nome)

        # Obter ou criar a categoria correspondente ao nome fornecido (se fornecida)
        categoria = None
        if categoria_nome:
            categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)

        # Atualizar os campos do objeto 'instance' com os dados fornecidos
        instance.nome_produto = validated_data.get('nome_produto', instance.nome_produto)
        instance.descricao = validated_data.get('descricao', instance.descricao)
        instance.preco = validated_data.get('preco', instance.preco)
        instance.estoque = validated_data.get('estoque', instance.estoque)
        instance.fabricante = fabricante
        instance.categoria = categoria
        instance.save()

        return instance