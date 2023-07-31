import os, json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from braintree import Subscription
from braintree.error_result import ErrorResult
from app_auth import models as AuthModels
from app_auth import mixins as AuthMixins
from payments import models as PaymentModels
import datetime
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from paypalrestsdk.notifications import WebhookEvent

from payments.utils.paypal import mode as mode

class PaymentView(View):
    template_name = "payments/index.html"
    context_data = dict()

# Create your views here.
class PaymentIndex(PaymentView):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass

class CompletePayment(PaymentView):
    def get(self, request, *args, **kwargs):
        return redirect(reverse("manager:pricings"))

    def post(self, request, *args, **kwargs):
        pricing_paypal_id = request.POST.get("pricing_paypal_id")
        selected_plan = PaymentModels.PaypalPlan.objects.filter(paypal_id=pricing_paypal_id).first()
        current_pricing = PaymentModels.PaypalSubscription.objects.filter(user=request.user.id).first()

        subscription = PaymentModels.PaypalSubscription.objects.filter(user=request.user.id).first()
        try:
            if subscription.plan.name.lower() != "Basic Monthly Package".lower():            
                ret = mode.myapi.post(f"v1/billing/subscriptions/{subscription.order_key}/suspend")
                if ret.get("error"):
                    messages.add_message(request, messages.ERROR, 'Opps! We are not able to cancel current subcription automatically.')
                    return redirect(reverse('manager:account'))
                else:
                    ret = mode.myapi.post(f"v1/billing/subscriptions/{subscription.order_key}/cancel")
                    messages.add_message(request, messages.ERROR, 'Opps! We are not able to cancel current subcription automatically.')
                    return redirect(reverse('manager:account'))

            data = {
                "plan_id": pricing_paypal_id
            }

            ret = mode.myapi.post("v1/billing/subscriptions", data)
            if ret.get("error"):
                messages.add_message(request, messages.ERROR, 'Unable to update your subscription. Contact support.')
                return redirect(reverse('manager:pricings'))

            if ret.get('status') == 'APPROVAL_PENDING':
                user = request.user
            
                subscription.previous_pricing = subscription.plan
                subscription.upgrading_to = selected_plan
                subscription.total_amount_paid=float(selected_plan.cost)
                subscription.order_key=ret['id']
                subscription.active=False

                subscription.expiry_date=timezone.now() + datetime.timedelta(days=30)

                subscription.save()

                redirect_url = mode.get_url_from(ret['links'], 'approve')

                return HttpResponseRedirect(redirect_url)
        except Exception as e:
            subscription.plan=current_pricing
            subscription.save()
            messages.add_message(request, messages.ERROR, 'Unable to update your subscription. Contact support.')
            return redirect(reverse('manager:pricings'))


def send_mail(email, message):
    email_body = render_to_string(
        "email_message.html",
        {
            "review": "{}".format(message),
        },
    )
    email = EmailMessage(
        "Ease Sell Extension",
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
    )
    
    email.send(fail_silently=False)

@require_POST
@csrf_exempt
def paypal_webhooks(request):
    transmission_id = request.headers['Paypal-Transmission-Id']
    timestamp = request.headers['Paypal-Transmission-Time']
    webhook_id = os.environ.get("PAYPAL_WEBHOOK_ID")
    event_body = request.body.decode('utf-8')
    cert_url = request.headers['Paypal-Cert-Url']
    auth_algo = request.headers['Paypal-Auth-Algo']
    actual_signature = request.headers['Paypal-Transmission-Sig']

    response = WebhookEvent.verify(
        transmission_id,
        timestamp,
        webhook_id,
        event_body,
        cert_url,
        actual_signature,
        auth_algo
    )
    if response:
        obj = json.loads(request.body)
        event_type = obj.get('event_type')
        resource = obj.get('resource')

    try:

        if resource.get("status", None) == 'APPROVAL_PENDING':
            billing_agreement_id = resource['id']
            subscription = PaymentModels.PaypalSubscription.objects.filter(order_key=billing_agreement_id).first()
            email = AuthModels.User.objects.filter(id=subscription.user.id).first().email
            send_mail(email, "Your payment as been initialized. Please wait for confirmation email.")

        elif resource.get("status", None) == 'ACTIVE':
            
            billing_agreement_id = resource['id']
            subscription = PaymentModels.PaypalSubscription.objects.filter(order_key=billing_agreement_id).first()
            email = AuthModels.User.objects.filter(id=subscription.user.id).first().email
            send_mail(email, "Your payment was successfull.")

            subscription.plan = subscription.upgrading_to
            subscription.payment_completed = True
            subscription.active=True
            subscription.save()

        elif resource.get("status", None) == "SUSPENDED":
            billing_agreement_id = resource['id']
            subscription = PaymentModels.PaypalSubscription.objects.filter(order_key=billing_agreement_id).first()
            ret = mode.myapi.post(f"v1/billing/subscriptions/{subscription.order_key}/cancel")
            send_mail(email, "Ease sell subscription deactivated successfully.")

        elif event_type == "BILLING.SUBSCRIPTION.CANCELLED":
            billing_agreement_id = resource['id']
            subscription = PaymentModels.PaypalSubscription.objects.filter(order_key=billing_agreement_id).first()
            email = AuthModels.User.objects.filter(id=subscription.user.id).first().email
            send_mail(email, "Ease sell subscription deactivated successfully.")

        return HttpResponse(status=200)
    except:
        pass

@csrf_exempt
def PaypalSubscriptionDeactivateView(request):
    try:
        if request.method == 'POST':
            package = PaymentModels.PaypalSubscription.objects.filter(user=request.user).first()
            subscription = PaymentModels.PaypalSubscription.objects.filter(user=request.user.id).first()

            ret = mode.myapi.post(f"v1/billing/subscriptions/{subscription.order_key}/suspend")

            if ret.get("error"):
                messages.add_message(request, messages.ERROR, 'Opps! Unable to deactivate, Try Again.')
                return redirect(reverse('manager:account'))

            subscription.plan = PaymentModels.PaypalPlan.objects.filter(name="Basic Monthly Package").first()
            subscription.expiry_date=timezone.now()
            subscription.total_amount_paid=0
            subscription.order_key="Not Set"
            subscription.active=False
            subscription.save()
            return redirect(reverse('manager:account'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Request.')
            return redirect(reverse('manager:home'))
    except Exception as E:
        messages.add_message(request, messages.ERROR, 'Please Try Again')
        return redirect(reverse('manager:home'))





class PaypalSubcribeView(PaymentView, AuthMixins.IsAuthenticatedAccessMixin):
    def post(self, request, *args, **kwargs):
        user = AuthModels.User.objects.filter(pk=request.user.pk)
        # create braintree customer

        # if user has not set first_name, last_name redirect to prompt page
        # stored the package he is paying for

        if not user.customer_payemnt_id:
            result = gateway.customer.create(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "company": "EASE-SELL",
                    "email": user.email,
                    "phone": user.get_moblie_number(),
                }
            )
            if result.is_success:
                user.customer_payemnt_id = result.customer.id
                user.save
        
        customer = gateway.customer.find(user.customer_payemnt_id)

            
    def get(self, request, *args, **kwargs):
        try:
            braintree_client_token = braintree.ClientToken.generate(
                {"customer_id": self.request.user.id}
            )
        except:
            braintree_client_token = braintree.ClientToken.generate({})

        self.context_data["braintree_client_token"] = braintree_client_token

        return render(request, self.template_name, context=self.context_data)