from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import MyUserCreationForm


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = "login.html"


class Logout(LogoutView):
    template_name = "logged_out.html"


class Register(CreateView):
    form_class = MyUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("shop:main")

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())
