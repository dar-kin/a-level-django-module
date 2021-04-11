from shop.forms import OrderForm, ReturnForm, CreateUpdateProductForm
from shop.models import Product, Order, Return
from myuser.models import MyUser
from django.test import testcases


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


class ReturnFormTest(testcases.TestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.product = Product.objects.create(name="1", description="", amount=10, cost=10)
        self.order = Order.objects.create(user=self.user, product=self.product, amount=10)
        self.correct_form = ReturnForm({"order": self.order})

    def test_correct_form_validation(self):
        self.assertTrue(self.correct_form.is_valid())

    def test_incorrect_form(self):
        ret_obj = Return.objects.create(order=self.order)
        self.correct_form.is_valid()
        self.assertEquals(self.correct_form.errors["__all__"][0], "This return already exists")


class ProductFormTest(testcases.TestCase):
    def setUp(self) -> None:
        self.correct_form = CreateUpdateProductForm({"name": "product", "amount": 100, "cost": 100})
        self.incorrect_form = CreateUpdateProductForm({"name": "product", "amount": 0, "cost": 0})
        self.incorrect_form1 = CreateUpdateProductForm({"name": "product", "amount": -10, "cost": -10})
        self.errors = {"cost": ["Invalid cost"], "amount": ["Invalid amount"], }

    def test_correct_form(self):
        self.assertTrue(self.correct_form.is_valid())

    def test_incorrect_form_with_zero(self):
        self.incorrect_form.is_valid()
        self.assertEquals(self.incorrect_form.errors, self.errors)

    def test_negative_values(self):
        self.incorrect_form1.is_valid()
        self.assertEquals(self.incorrect_form.errors, self.errors)

