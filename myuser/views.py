from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = "login.html"


class Logout(LogoutView):
    template_name = "logged_out.html"


class Register(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"


