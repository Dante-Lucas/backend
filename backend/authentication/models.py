from typing import Any
from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser ,UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):

        if not username or not email:
            raise ValueError("The given username and email must be set")
        
        email = self.normalize_email(email)
      
       
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                verbose_name='Nome de usuário',
                                db_column='nome_do_usuário',
                                help_text='Digite o username',)
    email = models.EmailField( max_length=254,
                              unique=True,
                              verbose_name='Email do usuário',
                              db_column='email',
                              help_text='Digite o email do usuário')
    data_nascimento = models.DateField(null=True,
                                       blank=True,
                                       verbose_name='Data de nascimento',
                                       db_column='data_de_nascimento',
                                       help_text='Digite sua data de nascimento')
    genero_choices = [
        ('M','Masculino'),
        ('F','Feminino'),
        ('O','Outro'),
        ('P','Prefiro não dizer'),
    ]
    genero = models.CharField(max_length=1,
                              choices=genero_choices,
                              null=True,
                              blank=True,
                              verbose_name='Gênero',
                              db_column='genero',
                              help_text='Gênero do usuário')
    telefone = models.CharField(max_length=20,
                                null=True,
                                blank=True,
                                db_column='telefone',
                                help_text='Digite seu número de celular ou telefone')
    

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    
    objects = UserManager()

    class Meta:
        db_table = 'Usuário'

    def __str__(self) -> str:
        return  self.username
    