from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, RedirectView, View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Product, Order, Return
from .forms import OrderForm, ReturnForm, CreateUpdateProductForm
from myuser.misc import SuperUserRequired
from .exceptions import NotEnoughMoneyException, NotEnoughProductException
from django.contrib import messages


class MainView(TemplateView):
    template_name = "main.html"


class ProductList(ListView):
    template_name = "product_list.html"
    model = Product
    extra_context = {"empty_form": OrderForm()}
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("invalid_product_number", False):
            context["invalid_product_number"] = self.request.session["invalid_product_number"]
            del self.request.session["invalid_product_number"]
        return context


class CreateOrder(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('shop:product_list')

    def form_valid(self, form):
        try:
            self.object = form.save()
            form.user.wallet -= self.object.total_cost
            form.product.amount -= self.object.amount
            form.user.save()
            form.product.save()
        except NotEnoughProductException:
            messages.add_message(self.request, messages.ERROR, "Not enough product")
        except NotEnoughMoneyException:
            messages.add_message(self.request, messages.ERROR, "Not enough money")
        else:
            messages.add_message(self.request, messages.SUCCESS, "Order created")
            return HttpResponseRedirect(self.get_success_url())
        return redirect(reverse("shop:product_list"))

    def form_invalid(self, form):
        self.request.session["invalid_product_number"] = form.product.id
        messages.add_message(self.request, messages.INFO, "Invalid amount")
        return redirect(reverse("shop:product_list"))


class OrderList(ListView):
    template_name = "order_list.html"
    model = Order
    paginate_by = 3
    extra_context = {"form": ReturnForm}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("invalid_return_creation", False):
            context["invalid_return_creation"] = self.request.session["invalid_return_creation"]
            del self.request.session["invalid_return_creation"]
        return context


class CreateReturn(CreateView):
    model = Return
    form_class = ReturnForm
    success_url = reverse_lazy('shop:orders')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Return has been requested")
        return super(CreateReturn, self).form_valid(form)

    def form_invalid(self, form):
        self.request.session["invalid_return_creation"] = form.order.id
        for key, value in form.errors.items():
            for elem in value:
                messages.add_message(self.request, messages.INFO, elem)
        return redirect(reverse("shop:orders"))


class ReturnSuccessView(TemplateView):
    template_name = "return_success.html"


class UpdateProductView(SuperUserRequired, UpdateView):
    model = Product
    form_class = CreateUpdateProductForm
    template_name = "product_update.html"
    success_url = reverse_lazy("shop:product_list")


class CreateProductView(SuperUserRequired, CreateView):
    model = Product
    form_class = CreateUpdateProductForm
    template_name = "product_add.html"
    success_url = reverse_lazy("shop:product_list")


class ReturnList(SuperUserRequired, ListView):
    template_name = "return_list.html"
    model = Return
    paginate_by = 3


class DeleteReturn(View):

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Return, id=request.POST.get("return"))
        if request.POST.get("approve", False):
            product = obj.order.product
            user = obj.order.user
            order = obj.order
            order_amount = order.amount
            order_total_cost = order.total_cost
            product.amount += order_amount
            user.wallet += order_total_cost
            user.save()
            product.save()
            obj.delete()
            order.delete()
            return render(request, "return_approved.html", {
                "user": user, "product": product,
                "order_amount": order_amount,
                "order_total_cost": order_total_cost
            })
        else:
            obj.delete()
            return redirect(reverse("shop:return_list"))


class RedirectToMainView(RedirectView):
    url = reverse_lazy("shop:main")