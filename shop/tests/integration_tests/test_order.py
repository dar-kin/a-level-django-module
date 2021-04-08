from django.test import TestCase, RequestFactory
from shop.models import Product, Order
from myuser.models import MyUser
from django.urls import reverse
from shop.views import CreateOrder
from shop.forms import OrderForm
from django.contrib import messages


class TestOrder(TestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.product = Product.objects.create(name="1", description="", amount=10, cost=10)
        self.correct_data = {"user": self.user, "product": self.product, "amount": 1}
        self.incorrect_data = {"user": self.user, "product": self.product, "amount": 0}
        self.client.force_login(self.user)

    def test_success_url(self):
        self.assertRedirects(self.client.post(reverse("shop:create_order"), data=self.correct_data),
                             expected_url=reverse("shop:product_list"))

    def test_unsuccess_url(self):
        self.assertRedirects(self.client.post(reverse("shop:create_order"), data=self.incorrect_data),
                             expected_url=reverse("shop:product_list"))
