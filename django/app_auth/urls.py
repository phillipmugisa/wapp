from django.urls import path
from app_auth import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "app_auth"

urlpatterns = [
    path("login/", views.loginUserView.as_view(), name="login"),
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("extension/keys/", views.ExtensionTasksViews.as_view(), name="extension_tasks"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", views.logout, name="logout"),
]
