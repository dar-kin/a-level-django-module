from django.urls import path
from .views import ProductList, MainView, OrderList, ReturnSuccessView, \
    UpdateProductView, ReturnList, CreateProductView, CreateOrder, CreateReturn, DeleteReturn, CeleryReturnView


app_name = "shop"

urlpatterns = [
    path("main", MainView.as_view(), name="main"),
    path("product_list", ProductList.as_view(), name="product_list"),
    path("orders", OrderList.as_view(), name="orders"),
    path("return_success", ReturnSuccessView.as_view(), name="return_success"),
    path("update_product/<int:pk>", UpdateProductView.as_view(), name="update_product"),
    path("return_list", ReturnList.as_view(), name="return_list"),
    path("add_product", CreateProductView.as_view(), name="add_product"),
    path("create_order", CreateOrder.as_view(), name="create_order"),
    path("create_return", CreateReturn.as_view(), name="create_return"),
    path("delete_return/<int:pk>", DeleteReturn.as_view(), name="delete_return"),
    path("aprrove_all_returns/", CeleryReturnView.as_view(), name="approve_all_returns"),
]