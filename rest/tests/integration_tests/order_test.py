from django.test import testcases
from rest_framework.test import APIClient
from shop.models import Order, Product
from myuser.models import MyUser
from rest.API.serializers import OrderSerializer


class TestApiLogin(testcases.TestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.client = APIClient()

    def test_401_for_anauthorized_user(self):
        response = self.client.post("rest/orders/", data={})
        print(response)
        self.assertEquals(self.client.post("/rest/orders/", data={}).status_code, 401)

    def test_token_authentication(self):
        response = self.client.post("/api-etoken-auth/", data={"username": "darkin", "password": 1}, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="EToken " + response.data['token'])
        self.assertEquals(self.client.post("/rest/orders/", data={}).status_code, 400)


class TestOrder(testcases.TestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="1")
        self.product = Product.objects.create(name="product", description="", cost=30, amount=100)
        self.client = APIClient()

    def authorized_request(self, target, data):
        self.client.credentials(HTTP_AUTHORIZATION="Basic " + "ZGFya2luOjE=")
        response = self.client.post(target, data)
        return response

    def test_order_creation(self):
        target = "/rest/orders/"
        data = {"user": 1, "product": 1, "amount": 5}
        response = self.authorized_request(target, data)
        self.assertEquals(response.status_code, 201)

    def test_invalid_data_creation(self):
        target = "/rest/orders/"
        data = {"user": 1, "product": 0, "amount": 5}
        response = self.authorized_request(target, data)
        self.assertEquals(response.status_code, 400)






