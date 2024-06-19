from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib import admin
from .models import User
from .forms import UserChangeForm,UserCreationForm

# Register your models here.



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações adicionais', 
         {'fields': (
             'data_nascimento',
                     'genero',
                     'telefone',
                     )
            }
        ),
    )
    