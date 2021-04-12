from django.db import models
from myuser.models import MyUser
from .exceptions import NotEnoughMoneyException, NotEnoughProductException, ReturnAlreadyExists, ReturnTimeExpired
from datetime import timedelta
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="products", blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    amount = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["create_date"]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.product.amount < self.amount:
            raise NotEnoughProductException
        elif self.total_cost > self.user.wallet:
            raise NotEnoughMoneyException
        self.user.wallet -= self.total_cost
        self.product.amount -= self.amount
        self.user.save()
        self.product.save()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def delete(self, using=None, keep_parents=False):
        self.user.wallet += self.total_cost
        self.product.amount += self.amount
        self.user.save()
        self.product.save()
        super().delete(using=None, keep_parents=False)

    @property
    def total_cost(self):
        return self.amount * self.product.cost


class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["create_date"]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if timezone.now() > self.order.create_date + timedelta(minutes=3):
            raise ReturnTimeExpired
        elif Return.objects.filter(order=self.order).exists():
            raise ReturnAlreadyExists
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def delete(self, using=None, keep_parents=False, approved=False):
        if approved:
            self.order.delete()
        super().delete(using=None, keep_parents=False)
