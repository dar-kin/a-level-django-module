from django.urls import path
from . import views


app_name = "myuser"


urlpatterns = [
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
]