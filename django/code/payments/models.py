from django.db import models
from app_auth import models as AuthModels
from django.utils.translation import gettext_lazy as _
import datetime, json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

# class Product(models.Model):
#     custom_id = models.CharField(_("Product Id"), max_length=256, null=True, blank=True)
#     name = models.CharField(_("Name"), max_length=256)
#     ProductType = models.CharField(_("Type"), max_length=256, default="Service")
#     description = models.TextField(_("Description"), max_length=256)

#     def __str__(self):
#         return f"{self.name}"

#     def save(self):
#         if not self.custom_id:
#             self.custom_id = "-".join(self.name.split(" "))
#         super().save()

#     def toJSON(self):
#         obj = {
#             "id" : self.custom_id,
#             "name" : self.name,
#             "service" : self.ProductType,
#             "description" : self.description,
#         }
#         return json.dumps(obj)

# BRAINTREE

class BraintreePlan(models.Model):
    plan_id = models.CharField(_("Plan Id"), max_length=256, default="0")
    name = models.CharField(_("name"), max_length=256, default="0")
    description = models.TextField(_("description"), default="0")
    billing_frequency = models.CharField(_("billing_frequency"), max_length=256, default="0")
    currency_iso_code = models.CharField(_("currency_iso_code"), max_length=256, default="0")
    Price = models.CharField(_("Price"), max_length=256, default="0")

    def __str__(self):
        return f"{self.name}"

class BraintreeSubscription(models.Model):
    class Meta:
        ordering = ['-id']

    user = models.ForeignKey(to=AuthModels.User, on_delete=models.CASCADE)
    plan = models.ForeignKey(to=BraintreePlan, on_delete=models.CASCADE)
    created_on = models.DateField(_("Created on"), default=datetime.date.today)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"


# PAYPAL
class PaypalSubscription(models.Model):
    class Meta:
        ordering = ['-id']

    user = models.ForeignKey(to=AuthModels.User, on_delete=models.CASCADE)
    plan = models.ForeignKey(to="PaypalPlan", on_delete=models.CASCADE)


    previous_pricing = models.ForeignKey(to="PaypalPlan", on_delete=models.CASCADE, blank=True, null=True, related_name="previous_pricing")
    upgrading_to = models.ForeignKey(to="PaypalPlan", on_delete=models.CASCADE, blank=True, null=True, related_name="upgrading_to")
    total_amount_paid = models.DecimalField(
        _("Total Amount Paid"), decimal_places=2, max_digits=8, blank=True, null=True,
    )
    start_date = models.DateField(_("Subscription Start Date"), default=datetime.date.today)
    expiry_date = models.DateField(_("Subscription Expiry Date"), blank=True, null=True)
    email = models.CharField(_("Client's Email"), max_length=256, blank=True, null=True)
    country_code = models.CharField(_("Client's Country"), max_length=9, blank=True, null=True)
    address = models.CharField(_("Client's Address"), max_length=256, blank=True, null=True)
    order_key = models.CharField(_("Order key"), max_length=256, blank=True, null=True)
    expired = models.BooleanField(_("Expired"), default=False)
    active = models.BooleanField(_("Active"), default=False)
    payment_completed = models.BooleanField(_("Payment Completed"), default=False)

    created_on = models.DateField(_("Created on"), default=datetime.date.today)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"

class PaypalProduct(models.Model):
    custom_id = models.CharField(_("Product Id"), max_length=256, null=True, blank=True)
    name = models.CharField(_("Name"), max_length=256)
    ProductType = models.CharField(_("Type"), max_length=256, default="Service")
    description = models.TextField(_("Description"), max_length=256)

    def __str__(self):
        return f"{self.name}"

    def save(self):
        if not self.custom_id:
            self.custom_id = "-".join(self.name.split(" "))
        super().save()

    def toJSON(self):
        obj = {
            "id" : self.custom_id,
            "name" : self.name,
            "service" : self.ProductType,
            "description" : self.description,
        }
        return json.dumps(obj)

class PaypalPlan(models.Model):
    paypal_id = models.CharField(_("Paypal ID"), max_length=256, null=True, blank=True)
    name = models.CharField(_("Plan Name"), max_length=256)
    status = models.CharField(_("Plan status"), max_length=256, default="ACTIVE")
    currency = models.CharField(_("Plan Currency"), max_length=256)
    product = models.ForeignKey(to=PaypalProduct, on_delete=models.CASCADE)
    cost = models.DecimalField(_("Plan Cost"), max_digits = 5,decimal_places = 2)
    description = models.TextField(_("Description"), max_length=256)
    interval_unit = models.CharField(_("Plan Duration"), max_length=256)
    interval_count = models.IntegerField(_("Interval Count"), default=1)
    subscribers = models.IntegerField(_("Plan Subscribers"), default=0)
    has_trial = models.BooleanField("Has Trial Period", default=False)

    def __str__(self):
        return f"{self.name}"

    def toJSON(self):
        obj = {
            "product_id": f"{self.product.custom_id}",
            "name": f"{self.name}",
            "description": f"{self.description}",
            "status": f"{self.status}",
            "billing_cycles": [
                {
                    "frequency": {
                    "interval_unit": f"{self.interval_unit}",
                    "interval_count": f"{self.interval_count}",
                    },
                    "tenure_type": "REGULAR",
                    "sequence": 2 if self.has_trial else 1,
                    "total_cycles": 0,
                    "pricing_scheme": {
                    "fixed_price": {
                        "value": f"{self.cost}",
                        "currency_code": f"{self.currency}",
                    }
                    }
                }
            ],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee": {
                    "value": "0",
                    "currency_code": f"{self.currency}",
                },
                "setup_fee_failure_action": "CONTINUE",
                "payment_failure_threshold": 3
            },
            "taxes": {
                "percentage": "0",
                "inclusive": False
            }
        }

        if self.has_trial:
            obj["billing_cycles"].append(
                {
                    "frequency": {
                    "interval_unit": "DAY",
                    "interval_count": 14
                    },
                    "tenure_type": "TRIAL",
                    "sequence": 1,
                    "total_cycles": 1,
                    "pricing_scheme": {
                    "fixed_price": {
                        "value": "0",
                        "currency_code": "USD"
                        }
                    }
                }
            )

        return obj


class Feature(models.Model):
    name = models.CharField(_("Name"), max_length=256)
    plan = models.ManyToManyField(to=PaypalPlan, related_name="pricing_feature")

    def __str__(self):
        return f'{self.name}'


# SIGNALS
@receiver(post_save, sender=BraintreeSubscription)
def on_braintree_subcription_create(sender, instance, *args, **kwargs):
    plan = instance.plan
    plan.subscribers += 1
    plan.save()

@receiver(post_delete, sender=BraintreeSubscription)
def on_braintree_subcription_delete(sender, instance, *args, **kwargs):
    plan = instance.plan
    plan.subscribers -= 1
    plan.save()

@receiver(post_save, sender=PaypalSubscription)
def on_paypal_subcription_create(sender, instance, *args, **kwargs):
    plan = instance.plan
    plan.subscribers += 1
    plan.save()

@receiver(post_delete, sender=PaypalSubscription)
def on_paypal_subcription_delete(sender, instance, *args, **kwargs):
    plan = instance.plan
    plan.subscribers -= 1
    plan.save()

@receiver(post_save, sender=AuthModels.User)
def on_subcription_create(sender, instance, *args, **kwargs):
    if instance.is_superuser:
        return
    if settings.PAYMENTMETHOD == "paypal":
        free_plan = PaypalPlan.objects.filter(name="Basic Monthly Package").first()
        if free_plan and not PaypalSubscription.objects.filter(user=instance):
            new_subscription = PaypalSubscription.objects.create(user=instance, plan=free_plan)
            new_subscription.save()
    elif settings.PAYMENTMETHOD == "braintree":
        free_plan = BraintreePlan.objects.filter(name="Basic Monthly Package").first()
        if free_plan:
            new_subscription = BraintreeSubscription.objects.create(user=instance, plan=free_plan)
            new_subscription.save()