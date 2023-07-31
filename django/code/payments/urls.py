from django.urls import path
from payments import views as PaymentsViews

app_name = "payments"

urlpatterns = [
    path("", PaymentsViews.PaymentIndex.as_view(), name="home"),
    path("paypalpayments/", PaymentsViews.CompletePayment.as_view(), name="paypalpayments"),
    path("paypal/deactivate/", PaymentsViews.PaypalSubscriptionDeactivateView, name="deactivate_paypal"),
    path('paypal-webhook/', PaymentsViews.paypal_webhooks, name='paypal_webhook'),
]