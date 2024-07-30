from django.urls import path
from . import views

urlpatterns = [
    path('produto/',views.ProdutoView.as_view(), name='adicionar'),
    path('produto/<int:id>/',views.ProdutoDetailsView.as_view(), name='detalhe'),
    path('categoria/',views.CategoriaView.as_view(), name='categoria'),
    path('fabricante/',views.FabricanteView.as_view(), name='fabricante')
]