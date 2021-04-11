from django.test import TestCase
from shop.models import Product, Order, Return
from myuser.models import MyUser
from shop.exceptions import NotEnoughMoneyException, NotEnoughProductException
from django.db.models import ObjectDoesNotExist


def get_fixture(name):
    return "fixtures/" + name


class TestOrder(TestCase):
    fixtures = [get_fixture("user.json"), get_fixture("product.json")]

    def setUp(self) -> None:
        self.product = Product.objects.get(id=1)
        self.product2 = Product.objects.get(id=2)
        self.user = MyUser.objects.get(id=1)
        self.user2 = MyUser.objects.get(id=2)
        self.test_order = Order(user=self.user, product=self.product, amount=10)
        self.test_order.save()
        self.user_test_zero_money = MyUser.objects.get(id=3)
        self.product_test_zero_amount = Product.objects.get(id=3)
        Order.objects.create(user=self.user_test_zero_money, product=self.product_test_zero_amount, amount=100)

    def test_correct_update_user_money(self):
        self.assertEqual(self.user.wallet, 10000 - self.test_order.total_cost)

    def test_correct_total_cost(self):
        self.assertEqual(self.test_order.total_cost, 10 * self.product.cost)

    def test_correct_update_product_amount(self):
        self.assertEqual(100 - self.test_order.amount, self.product.amount)

    def test_correct_exception_for_not_enough_money(self):
        test_incorrect_order_amount = Order(user=self.user, product=self.product2, amount=15)
        with self.assertRaises(NotEnoughMoneyException):
            test_incorrect_order_amount.save()

    def test_correct_exception_for_not_enough_product(self):
        test_incorrect_order_amount = Order(user=self.user2, product=self.product, amount=101)
        with self.assertRaises(NotEnoughProductException):
            test_incorrect_order_amount.save()

    def test_possibility_to_have_zero_money_after_order(self):
        self.assertEqual(self.user_test_zero_money.wallet, 0)

    def test_possibility_to_have_zero_amount_after_order(self):
        self.assertEqual(self.product_test_zero_amount.amount, 0)

class TestOderDeletion(TestCase):
    fixtures = [get_fixture("user.json"), get_fixture("product.json")]

    def setUp(self) -> None:
        self.user = MyUser.objects.get(id=1)
        self.product = Product.objects.get(id=1)
        self.order = Order.objects.create(user=self.user, product=self.product, amount=10)
        self.order.delete()

    def test_user_received_money_back(self):
        self.assertEqual(self.user.wallet, 10000)

    def test_product_received_amount_back(self):
        self.assertEqual(self.product.amount, 100)


class ReturnDeletion(TestCase):
    fixtures = [get_fixture("user.json"), get_fixture("product.json")]

    def setUp(self) -> None:
        user = MyUser.objects.get(id=1)
        product = Product.objects.get(id=1)
        test_order = Order.objects.create(user=user, product=product, amount=10)
        test_order1 = Order.objects.create(user=user, product=product, amount=10)
        return1 = Return.objects.create(order=test_order)
        return2 = Return.objects.create(order=test_order1)
        return1.delete(approved=True)
        return2.delete(approved=False)

    def test_approved_return(self):
        with self.assertRaises(ObjectDoesNotExist):
            Order.objects.get(id=1)

    def test_deleted_return(self):
        self.assertEquals(len(Order.objects.filter(id=2)), 1)

