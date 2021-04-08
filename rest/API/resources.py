from rest_framework.viewsets import ModelViewSet
from .serializers import SimpleOrderSerializer, ProductSerializer, ReturnSerializer
from myuser.models import MyUser
from shop.models import Product, Order, Return
from rest.misc import IsAdminOrReadOnly, OrderPermission, ReturnPermission
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class OrderViewSet(ModelViewSet):
    serializer_class = SimpleOrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, OrderPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReturnViewSet(ModelViewSet):
    serializer_class = ReturnSerializer
    queryset = Return.objects.all()
    permission_classes = [IsAuthenticated, ReturnPermission]
