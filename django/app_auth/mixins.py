from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin

class IsAuthenticatedAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("app_auth:login"))
        return super().dispatch(request, *args, **kwargs)