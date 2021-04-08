from django.test import testcases
from myuser.models import MyUser
from django.urls import reverse


class LoginTest(testcases.TestCase):
    def setUp(self) -> None:
        self.user = MyUser.objects.create_user(username="darkin", password="123")
        self.correct_data = {"username": "darkin", "password": "123"}

    def test_correct_login_redirect(self):
        self.assertRedirects(self.client.post(reverse("myuser:login"), data=self.correct_data), reverse("shop:main"))

    def test_redirect_authenticated_user(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse("myuser:login")), reverse("shop:main"))
