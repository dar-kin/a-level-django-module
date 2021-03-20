from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Product, Order, Return
from .forms import OrderForm, ReturnForm, CreateUpdateProductForm
from myuser.misc import SuperUserRequired


class MainView(TemplateView):
    template_name = "main.html"


class ProductList(ListView):
    template_name = "product_list.html"
    model = Product
    extra_context = {"form": OrderForm()}
    paginate_by = 3

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("myuser:login"))
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.total_cost > request.user.wallet:
                form.add_error("amount", "Not enough money")
            else:
                request.user.wallet -= order.total_cost
                form.product.amount -= order.amount
                request.user.save()
                form.product.save()
                order.save()
                return redirect(reverse("shop:orders"))

        context = {"object_list": self.get_queryset(), "form": OrderForm(),
                   "product": int(request.POST.get("product")), "error_form": form}
        return render(request, "product_list.html", context)


class OrderList(ListView):
    template_name = "order_list.html"
    model = Order
    paginate_by = 3

    def post(self, request, *args, **kwargs):
        form = ReturnForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("shop:return_success"))
        return render(request, "order_list.html", context={"object_list": self.get_queryset(),
                                                           "form": ReturnForm(),
                                                           "order": int(request.POST.get("order")),
                                                           "error_form": form})


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
