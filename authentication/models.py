from typing import Any
from django.db import models
from django.apps import apps
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    UserManager as BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username or not email:
            raise ValueError('The given username and email must be set')

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self, username, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Nome de usuário',
        db_column='nome_do_usuário',
        help_text='Digite o username',
        validators=[username_validator],
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email do usuário',
        db_column='email',
        help_text='Digite o email do usuário',
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    data_nascimento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de nascimento',
        db_column='data_de_nascimento',
        help_text='Digite sua data de nascimento',
    )
    genero_choices = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('P', 'Prefiro não dizer'),
    ]
    genero = models.CharField(
        max_length=1,
        choices=genero_choices,
        null=True,
        blank=True,
        verbose_name='Gênero',
        db_column='genero',
        help_text='Gênero do usuário',
    )
    telefone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        db_column='telefone',
        help_text='Digite seu número de celular ou telefone',
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'Usuário'

    def __str__(self) -> str:
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
