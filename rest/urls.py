from .API.resources import ProductViewSet, OrderViewSet, ReturnViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'returns', ReturnViewSet)
urlpatterns = router.urls