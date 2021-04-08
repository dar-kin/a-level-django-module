from shop.forms import OrderForm
from shop.models import Product
from myuser.models import MyUser
from django.test import testcases
from django.urls import reverse


class OrderFormTest(testcases.TestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.product = Product.objects.create(name="1", description="", amount=10, cost=10)
        self.correct_form = OrderForm({"user": self.user, "product": self.product, "amount": 1})
        self.incorrect_form = OrderForm({"user": self.user, "product": self.product, "amount": 0})

    def test_form_with_valid_amount(self):
        self.assertTrue(self.correct_form.is_valid())

    def test_form_with_invalid_amount(self):
        self.assertFalse(self.incorrect_form.is_valid())

    def test_form_with_invalid_amount_error_message(self):
        self.assertEquals(self.incorrect_form.errors["amount"][0], "Invalid amount")

