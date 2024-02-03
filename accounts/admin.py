from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .form import CustomeUserChangeForm, CustomeUserCreationForm

@admin.register(CustomUser)
class CustomeUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomeUserChangeForm
    add_form = CustomeUserCreationForm
    list_display = ('username', 'email')


