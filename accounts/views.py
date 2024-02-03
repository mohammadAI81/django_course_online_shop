from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.conf import settings

from .form import CustomUserCreationForm
from .models import CustomUser


class Signup(CreateView):
    model = CustomUser
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
