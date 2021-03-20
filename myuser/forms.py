from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        fields = ("username", )
        model = MyUser
