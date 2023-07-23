from django.urls import path
from manager import views as ManagerViews

app_name = "manager"

urlpatterns = [
    path("", ManagerViews.HomePageView.as_view(), name="home"),
    path("pricings/", ManagerViews.PricingView.as_view(), name="pricings"),
    path("account/", ManagerViews.AccountView.as_view(), name="account"),
    path("whatsapp/", ManagerViews.WhatsappView.as_view(), name="whatsapp-view"),
]