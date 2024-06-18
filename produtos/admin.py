from django.contrib import admin
from .models import Produto,Fabricante,Categoria
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Fabricante)
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id','nome_produto','estoque','categoria','preco']
    list_filter = ['fabricante','categoria']