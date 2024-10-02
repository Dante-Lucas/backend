from . import Fabricante, Categoria
from django.db import models
from authentication.models import User


class Produto(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nome_produto = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    fabricante = models.ForeignKey(Fabricante, on_delete=models.PROTECT)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nome_produto
