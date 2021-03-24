from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, RedirectView, DeleteView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Product, Order, Return
from .forms import OrderForm, ReturnForm, CreateUpdateProductForm
from myuser.misc import SuperUserRequired
from .exceptions import NotEnoughMoneyException, NotEnoughProductException
from django.contrib import messages
from .misc import check_invalid_form


class MainView(TemplateView):
    template_name = "main.html"


class ProductList(ListView):
    template_name = "product_list.html"
    model = Product
    extra_context = {"empty_form": OrderForm()}
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return check_invalid_form(self.request, context, OrderForm)


class CreateOrder(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('shop:product_list')

    def form_valid(self, form):
        try:
            self.object = form.save()
        except NotEnoughProductException:
            messages.add_message(self.request, messages.ERROR, "Not enough product")
        except NotEnoughMoneyException:
            messages.add_message(self.request, messages.ERROR, "Not enough money")
        else:
            messages.add_message(self.request, messages.SUCCESS, "Order created")
            return HttpResponseRedirect(self.get_success_url())
        return redirect(reverse("shop:product_list"))

    def form_invalid(self, form):
        self.request.session['errors'] = form.errors
        self.request.session["invalid_form_number"] = form.product.id
        return redirect(reverse("shop:product_list"))


class OrderList(ListView):
    template_name = "order_list.html"
    model = Order
    paginate_by = 3
    extra_context = {"form": ReturnForm}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return check_invalid_form(self.request, context, ReturnForm)


class CreateReturn(CreateView):
    model = Return
    form_class = ReturnForm
    success_url = reverse_lazy('shop:orders')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Return has been requested")
        return super(CreateReturn, self).form_valid(form)

    def form_invalid(self, form):
        self.request.session['errors'] = form.errors
        self.request.session["invalid_form_number"] = form.order.id
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


class DeleteReturn(DeleteView):
    success_url = reverse_lazy("shop:return_list")
    model = Return

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        approve = request.POST.get("approve", False)
        self.object.delete(approved=approve)
        if approve:
            messages.add_message(request, messages.SUCCESS, "Return was approved")
        else:
            messages.add_message(request, messages.SUCCESS, "Return was discarded")
        return HttpResponseRedirect(success_url)


class RedirectToMainView(RedirectView):
    url = reverse_lazy("shop:main")