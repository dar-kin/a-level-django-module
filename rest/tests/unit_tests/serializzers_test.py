from django.test import testcases
from myuser.models import MyUser
from shop.models import Product, Order
from rest.API.serializers import SimpleOrderSerializer


class TestOrderSerializer(testcases.TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(name="1", description="", amount=10, cost=10)
        self.correct_serializer = SimpleOrderSerializer(data={"product": self.product.id, "amount": 1})
        self.incorrect_serializer = SimpleOrderSerializer(data={"product": self.product.id, "amount": 0})

    def test_serializer_with_valid_amount(self):
        self.assertTrue(self.correct_serializer.is_valid())

    def test_serializer_with_invalid_amount(self):
        self.assertFalse(self.incorrect_serializer.is_valid())

    def test_serializer_with_invalid_amount_error_message(self):
        self.incorrect_serializer.is_valid()
        self.assertEquals(self.incorrect_serializer.errors["amount"][0], "Invalid amount")