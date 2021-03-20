from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    wallet = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=10000)

    def __str__(self):
        return self.username
