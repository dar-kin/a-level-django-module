from django.db import models
from myuser.models import MyUser


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    amount = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["create_date"]

    @property
    def total_cost(self):
        return self.amount * self.product.cost


class Return(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["create_date"]
