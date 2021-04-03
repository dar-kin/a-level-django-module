from django.contrib import admin
from rest_framework.authtoken import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop.views import RedirectToMainView
from rest.views import CustomAuthToken

urlpatterns = [
    path("myuser/", include("myuser.urls", namespace="myuser")),
    path('admin/', admin.site.urls),
    path("shop/", include("shop.urls", namespace="shop")),
    path("rest/", include("rest.urls")),
    path('api-etoken-auth/', CustomAuthToken.as_view()),
    path("", RedirectToMainView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
