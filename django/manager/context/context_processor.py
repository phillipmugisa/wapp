from payments import models as PaymentModels
from django.conf import settings

def user_subcription(request):
    context = dict()
    if request.user.is_authenticated:
        if settings.PAYMENTMETHOD == "paypal":
            context["user_subsciption"] = PaymentModels.PaypalSubscription.objects.filter(user=request.user).first()
        elif settings.PAYMENTMETHOD == "braintree":
            context["user_subsciption"] = PaymentModels.BraintreeSubscription.objects.filter(user=request.user).first()
    return context