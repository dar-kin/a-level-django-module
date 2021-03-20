from django.forms import ModelForm, ImageField
from .models import Order, Return, Product
from django.forms import HiddenInput
from datetime import timedelta
from django.utils import timezone


class OrderForm(ModelForm):
    class Meta:
        fields = ["user", "product", "amount"]
        model = Order
        widgets = {'user': HiddenInput(),
                   'product': HiddenInput()}

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        self.product = self.cleaned_data.get("product")
        if amount > self.product.amount:
            self.add_error("amount", "Not enough items in storage")
        if amount <= 0:
            self.add_error("amount", "Invalid amount")
        return amount


class ReturnForm(ModelForm):

    def clean(self):
        order = self.cleaned_data.get("order")
        if timezone.now() > order.create_date + timedelta(minutes=3):
            self.add_error(None, "Return time expired")
        elif Return.objects.filter(order=order).exists():
            self.add_error(None, "This return already exists")

    class Meta:
        fields = ["order"]
        model = Return
        widgets = {
            "order": HiddenInput()
        }


class CreateUpdateProductForm(ModelForm):
    photo = ImageField(label="Upload image")

    def clean(self):
        cleaned_data = super().clean()
        cost = cleaned_data.get("cost")
        amount = cleaned_data.get("amount")
        if amount < 0:
            self.add_error("amount", "Invalid amount")
        if cost < 0:
            self.add_error("cost", "Invalid cost")

    class Meta:
        model = Product
        fields = ("name", "description", "cost", "amount")
