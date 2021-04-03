from rest_framework import permissions
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from .models import ExpiringToken


def safe_or_admin(request):
    if request.method in permissions.SAFE_METHODS:
        return True

    return request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return safe_or_admin(request)

    def has_permission(self, request, view):
        return safe_or_admin(request)


class OrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return safe_or_admin(request)

    def has_permission(self, request, view):
        return safe_or_admin(request) or request.method == "POST"


class ReturnPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

    def has_permission(self, request, view):
        return request.user.is_superuser or request.method == "POST"


class ExpiringTokenAuthentication(TokenAuthentication):
    keyword = "EToken"
    model = ExpiringToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if (timezone.now() - token.last_action).seconds > settings.TOKEN_EXPIRING_TIME:
            token.key = ExpiringToken.generate_key()
            token.delete()
            raise AuthenticationFailed("Token has expired. Please, obtain a new one.")
        token.save()
        return user, token


