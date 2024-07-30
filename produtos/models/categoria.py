from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nome