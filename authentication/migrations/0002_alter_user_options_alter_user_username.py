# Generated by Django 5.0.6 on 2024-06-27 16:58

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_column='nome_do_usuário', help_text='Digite o username', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Nome de usuário'),
        ),
    ]
