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
        self.user = self.cleaned_data.get("user")
        if amount <= 0:
            self.add_error("amount", "Invalid amount")
        return amount


class ReturnForm(ModelForm):

    def clean(self):
        self.order = self.cleaned_data.get("order")
        if timezone.now() > self.order.create_date + timedelta(minutes=3):
            self.add_error(None, "Return time expired")
        elif Return.objects.filter(order=self.order).exists():
            self.add_error(None, "This return already exists")

    class Meta:
        fields = ["order"]
        model = Return
        widgets = {
            "order": HiddenInput()
        }


class CreateUpdateProductForm(ModelForm):

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
        fields = ("name", "description", "cost", "amount", "photo")
