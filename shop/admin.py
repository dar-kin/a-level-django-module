from django.contrib import admin
from .models import Product, Order, Return


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ["name", "description", "cost", "amount"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ["user", "product", "amount"]


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    fields = ["order", ]