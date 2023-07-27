from django.urls import path, include
from app_api import views as ApiViews

from rest_framework.routers import DefaultRouter

app_name = "app_api"

urlpatterns = [
    path("whatsapp/schedule/", ApiViews.WhatsappSchedulerView, name="whatsapp-scheduler"),
]