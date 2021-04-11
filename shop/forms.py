from django.forms import ModelForm, ImageField
from django.forms import ValidationError
from .models import Order, Return, Product
from django.forms import HiddenInput


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
            raise ValidationError("Invalid amount")
        return amount


class ReturnForm(ModelForm):

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
        if amount <= 0:
            self.add_error("amount", "Invalid amount")
        if cost <= 0:
            self.add_error("cost", "Invalid cost")

    class Meta:
        model = Product
        fields = ("name", "description", "cost", "amount", "photo")
