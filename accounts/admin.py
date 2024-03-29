from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .form import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username', 'email')


