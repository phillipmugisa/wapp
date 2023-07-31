
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from manager.views import HomePageView

urlpatterns = [
    path("", include("manager.urls", namespace="manager")),
    path("auth/", include("app_auth.urls", namespace="app_auth")),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("accounts/profile/", HomePageView.as_view()),
    path("api/", include("app_api.urls", namespace="app_api")),
    path("payments/", include("payments.urls", namespace="payments")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)