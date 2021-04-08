from django.test import testcases
from shop.misc import check_invalid_form
from shop.forms import OrderForm


class MiscTest(testcases.TestCase):
    class Request:
        session = {}

        def fill_session(self, **kwargs):
            for key, value in kwargs.items():
                self.session[key] = value

    def perform_check_invalid_form(self):
        request = self.Request()
        request.fill_session(errors={"amount": ["Invalid amount"]}, invalid_form_number=1)
        context = {}
        context = check_invalid_form(request, context, OrderForm)
        return request, context

    def test_check_invalid_form_clear_session(self):
        request, context = self.perform_check_invalid_form()
        self.assertFalse(request.session)

    def test_check_invalid_form_modify_context(self):
        request, context = self.perform_check_invalid_form()
        self.assertTrue(context)

    def test_check_invalid_form_context_form(self):
        errors = {"amount": ["Invalid amount"]}
        request, context = self.perform_check_invalid_form()
        self.assertEquals(errors, context["error_form"]._errors)

    def test_check_invalid_form_context_number(self):
        request, context = self.perform_check_invalid_form()
        self.assertEquals(1, context["invalid_form_number"])



