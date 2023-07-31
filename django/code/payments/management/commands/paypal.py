import os
import json
import logging

from django.core.management.base import BaseCommand

from payments.utils.paypal import mode as mode
from payments import models as PaymentModels

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    help = """
        Manages Paypal Plans and Products
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--create",
            "-c",
            choices=[mode.PRODUCT, mode.PLAN],
            help="Creates Paypal product or plan"
        )
        parser.add_argument(
            "--list",
            "-l",
            choices=[mode.PRODUCT, mode.PLAN],
            help="List Paypal products or plans"
        )

    def create_product(self):
        with open(mode.PRODUCT_CONF_PATH, "r") as f:
            product = json.load(f)
            ret = mode.myapi.post("v1/catalogs/products", product)
            
            if "error" not in ret.keys():
                product = PaymentModels.PaypalProduct(
                    custom_id=product['id'],
                    name=product['name'],
                    ProductType=product['type'],
                    description=product['description']
                )
                product.save()
                print(product.name)
            else:
                print("Product not created.")
                

    def create_plan(self):
        with open(mode.PLAN_CONF_PATH, "r") as f:
            data = json.load(f)
            for plan in data:
                product = PaymentModels.PaypalProduct.objects.filter(custom_id=plan["product"])
                if not product:
                    print(f"Product with id {plan['product']} not Found")
                    break
                plan = PaymentModels.PaypalPlan(
                    name = plan["name"],
                    status = plan["status"],
                    currency = plan["currency"],
                    product = product.first(),
                    cost = plan["cost"],
                    description = plan["description"],
                    interval_unit = plan["interval_unit"],
                    interval_count = plan["interval_count"],
                    has_trial = plan["has_trial"],
                )
                plan.save()

                if plan.cost == "0.0":
                    continue
                
                ret = mode.myapi.post("v1/billing/plans", plan.toJSON())

                if "error" in ret.keys():
                    plan.delete()
                    print(f"Error Creating Plan {plan.name}")
                    break
                else:
                    plan.paypal_id = ret.get("id")
                    plan.save()
                    print(plan)

    def list_product(self):
        ret = mode.myapi.get("v1/catalogs/products")
        print(ret)
        logger.debug(ret)

    def list_plan(self):
        ret = mode.myapi.get("v1/billing/plans")
        print(ret)
        logger.debug(ret)

    def create(self, what):
        if what == mode.PRODUCT:
            self.create_product()
        else:
            self.create_plan()

    def list(self, what):
        if what == mode.PRODUCT:
            self.list_product()
        else:
            self.list_plan()

    def handle(self, *args, **options):
        create_what = options.get("create")
        list_what = options.get("list")

        if create_what:
            logger.debug(f"Create a {create_what}")
            self.create(create_what)
        elif list_what:
            logger.debug(f"List {list_what}")
            self.list(list_what)
